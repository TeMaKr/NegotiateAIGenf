import hashlib
import logging
from datetime import datetime
from ipaddress import ip_address
from typing import Tuple

from ratelimit.auths import EmptyInformation
from ratelimit.backends.redis import RedisBackend
from ratelimit.types import Scope
from redis.asyncio import StrictRedis
from settings import settings

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def is_ip_valid(ip: str) -> bool:
    """
    helper to determine whether ip is a global ip or part of an allowed subnet
    """
    parsed_ip = ip_address(ip.strip())
    return (
        parsed_ip.is_global
        or settings.rate_limit.rate_limit_allowed_subnet is not None
        and parsed_ip in settings.rate_limit.rate_limit_allowed_subnet
    )


async def client_ip(scope: Scope) -> Tuple[str, str]:
    """
    parse ip from starlette scope, consider "unreal" ip when testing.
    """

    # Step 1: Check for client IP in scope
    real_ip = ""
    if scope["client"]:
        ip, _ = tuple(scope["client"])
        if is_ip_valid(ip):
            real_ip = ip
        elif settings.environment.environment in ["DEVELOPMENT", "LOCAL"]:
            # Allow Docker internal IPs in development/local environments
            real_ip = ip

    # Step 2: Check for x-real-ip header
    for name, value in scope["headers"]:
        if name == b"x-real-ip":
            ip = value.decode("utf8")
            try:
                if not real_ip and is_ip_valid(ip):  # type: ignore
                    real_ip = ip  # type: ignore
            except Exception:
                # If the ip is not valid, we ignore it.
                # This can happen if the ip is malformed or not a valid IP address.
                pass

    forwarded_ip = None
    if len(settings.rate_limit.rate_limit_trusted_proxies_list) > 0:
        for name, value in scope["headers"]:
            if name == b"x-forwarded-for":
                # iterate over all forwarded ips from the rightmost
                forwarded_ips = value.decode("utf8").split(",")[::-1]
                for fip in forwarded_ips:
                    fip = fip.strip()
                    if fip in settings.rate_limit.rate_limit_trusted_proxies_list:
                        continue
                    if is_ip_valid(fip):
                        forwarded_ip = fip
                        break
                if not real_ip and forwarded_ip:
                    real_ip = forwarded_ip

    if not real_ip:
        raise EmptyInformation(scope)
    logger.info(f"Using IP {real_ip} for rate limiting.")
    return real_ip, "default"


def get_user_agent(scope: Scope) -> str:
    """
    Extract user agent from request headers
    """
    for name, value in scope["headers"]:
        if name == b"user-agent":
            return value.decode("utf8")
    return "unknown"


async def hash_based_auth(scope: Scope) -> Tuple[str, str]:
    """
    Create a hash-based authentication using daily salt + domain + IP + user agent
    Format: hash(daily_salt + website_domain + ip_address + user_agent)
    """
    # Get the current date as daily salt (YYYY-MM-DD format)
    daily_salt = datetime.now().strftime("%Y-%m-%d")

    # Extract IP address using existing logic
    real_ip = ""
    if scope["client"]:
        ip, _ = tuple(scope["client"])
        if is_ip_valid(ip):
            real_ip = ip
        elif settings.environment.environment in ["DEVELOPMENT", "LOCAL"]:
            # Allow Docker internal IPs in development/local environments
            real_ip = ip

    # Handle forwarded IP headers
    for name, value in scope["headers"]:
        if name == b"x-real-ip":
            ip = value.decode("utf8")
        try:
            if not real_ip and is_ip_valid(ip):  # type: ignore
                real_ip = ip  # type: ignore
        except Exception:
            # If the ip is not valid, we ignore it.
            pass

    # Handle X-Forwarded-For header
    forwarded_ip = None
    if len(settings.rate_limit.rate_limit_trusted_proxies_list) > 0:
        for name, value in scope["headers"]:
            if name == b"x-forwarded-for":
                # iterate over all forwarded ips from the rightmost
                forwarded_ips = value.decode("utf8").split(",")[::-1]
                for fip in forwarded_ips:
                    fip = fip.strip()
                    if fip in settings.rate_limit.rate_limit_trusted_proxies_list:
                        continue
                    if is_ip_valid(fip):
                        forwarded_ip = fip
                        break
                if not real_ip and forwarded_ip:
                    real_ip = forwarded_ip

    if not real_ip:
        raise EmptyInformation(scope)

    user_agent = get_user_agent(scope)

    # Create the hash string: daily_salt + domain + ip + user_agent
    hash_input = f"{daily_salt}:{real_ip}:{user_agent}"

    # Create SHA256 hash
    hash_value = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    return hash_value, "default"


redis_instance = StrictRedis(
    host=settings.redis.host,
    port=settings.redis.port,
)

redis_backend = RedisBackend(redis_instance)

# Use hash-based authentication method instead of simple IP-based
auth_method = hash_based_auth
