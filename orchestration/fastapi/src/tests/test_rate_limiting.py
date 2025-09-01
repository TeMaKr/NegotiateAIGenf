import logging
import random
import time
from typing import Dict

import httpx

"""Rate limiting tests for the health endpoint (development environment)"""

"""Tests are written with Claude """

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
URL = "https://dev-negotiate-ai.social-data-company.de/api/api/ping"
RATE_LIMIT = 5  # requests per minute
TIME_WINDOW = 60  # seconds


def get_random_ip() -> str:
    """Generate a random IP address for testing"""
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"


def single_request(request_id: int, timeout: int = 30, **kwargs) -> Dict:
    """Make a single HTTP request with various identification methods"""
    start_time = time.time()

    # Prepare headers
    headers = {"Content-Type": "application/json"}

    # Extract parameters
    ip_address = kwargs.get("ip_address")
    user_agent = kwargs.get("user_agent")

    # Add IP headers (test if server uses these vs real connection IP)
    if ip_address:
        headers["X-Forwarded-For"] = ip_address
        headers["X-Real-IP"] = ip_address

    # Add user agent
    if user_agent:
        headers["User-Agent"] = user_agent
    else:
        headers["User-Agent"] = "python-httpx-test-client"

    try:
        response = httpx.get(url=URL, headers=headers, timeout=timeout)
        end_time = time.time()

        return {
            "request_id": request_id,
            "status_code": response.status_code,
            "response_time": round((end_time - start_time) * 1000, 2),
            "success": response.status_code == 200,
            "headers": dict(response.headers),
            "error": None,
            **kwargs,
        }
    except Exception as e:
        end_time = time.time()
        return {
            "request_id": request_id,
            "status_code": getattr(e, "response", {}).get("status_code", 0)
            if hasattr(e, "response")
            else 0,
            "response_time": round((end_time - start_time) * 1000, 2),
            "success": False,
            "headers": {},
            "error": str(e),
            **kwargs,
        }


def test_single_request():
    """Test that a single request works correctly"""
    result = single_request(0, timeout=30)

    if result["success"]:
        logger.info("Single request works correctly")
    else:
        logger.warning(
            f"Single request failed: {result['status_code']} - {result['error']}"
        )


def test_basic_rate_limiting():
    """Test basic rate limiting with same user agent - should hit rate limit"""
    results = []
    user_agent = "python-httpx-test-client"

    for i in range(8):
        result = single_request(request_id=i, user_agent=user_agent)
        results.append(result)

    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful

    logger.info(f"Basic rate limiting results: {successful}/{len(results)} successful")

    if successful <= RATE_LIMIT and failed > 0:
        logger.info("Rate limiting works correctly - blocks requests after limit")
    elif successful > RATE_LIMIT:
        logger.warning(
            f"Rate limiting may not be working - got {successful} successful requests, expected <= {RATE_LIMIT}"
        )
    elif failed == 0:
        logger.warning("Rate limiting not working - no requests were blocked")


def test_ip_header_bypass():
    """Test if fake IP headers can bypass rate limiting - should NOT work"""
    results = []
    user_agent = "python-httpx-test-client"

    for i in range(8):
        fake_ip = get_random_ip()
        result = single_request(request_id=i, ip_address=fake_ip, user_agent=user_agent)
        results.append(result)

    successful = sum(1 for r in results if r["success"])

    logger.info(f"IP header bypass results: {successful}/{len(results)} successful")

    if successful <= RATE_LIMIT:
        logger.info(
            "Real IP is used correctly - fake IP headers cannot bypass rate limiting"
        )
    else:
        logger.warning(
            f"IP header bypass worked! Got {successful} successful requests, expected <= {RATE_LIMIT}"
        )


def test_user_agent_bypass():
    """Test if changing User-Agent can bypass rate limiting - should currently work"""
    results = []
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) Firefox/89.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)",
        "PostmanRuntime/7.28.4",
        "curl/7.68.0",
        "python-requests/2.28.1",
        "httpx/0.24.0",
    ]

    for i in range(8):
        user_agent = user_agents[i % len(user_agents)]
        result = single_request(request_id=i, user_agent=user_agent)
        results.append(result)

    successful = sum(1 for r in results if r["success"])

    logger.info(f"User-Agent bypass results: {successful}/{len(results)} successful")

    if successful >= 7:
        logger.info(
            "User-Agent rotation successfully bypasses rate limiting as expected"
        )
    elif successful <= RATE_LIMIT:
        logger.warning(
            f"User-Agent bypass did not work - got {successful} successful requests, expected >= 7"
        )
    else:
        logger.warning(
            f"User-Agent bypass partially worked - got {successful} successful requests"
        )


def test_no_user_agent():
    """Test what happens with no User-Agent header"""
    results = []

    for i in range(6):
        # Make request without User-Agent header
        start_time = time.time()
        headers = {"Content-Type": "application/json"}

        try:
            response = httpx.get(url=URL, headers=headers, timeout=30)
            end_time = time.time()

            result = {
                "request_id": i,
                "status_code": response.status_code,
                "response_time": round((end_time - start_time) * 1000, 2),
                "success": response.status_code == 200,
                "headers": dict(response.headers),
                "error": None,
                "user_agent": "NONE",
            }
        except Exception as e:
            end_time = time.time()
            result = {
                "request_id": i,
                "status_code": 0,
                "response_time": round((end_time - start_time) * 1000, 2),
                "success": False,
                "headers": {},
                "error": str(e),
                "user_agent": "NONE",
            }

        results.append(result)

    successful = sum(1 for r in results if r["success"])

    logger.info(f"No User-Agent results: {successful}/{len(results)} successful")

    if successful <= RATE_LIMIT:
        logger.info(
            "Rate limiting works even without User-Agent - server handles missing User-Agent gracefully"
        )
    else:
        logger.warning(
            f"Rate limiting may not work without User-Agent - got {successful} successful requests, expected <= {RATE_LIMIT}"
        )


if __name__ == "__main__":
    logger.info("Starting rate limiting tests")
    test_single_request()
    test_basic_rate_limiting()
    test_ip_header_bypass()
    test_user_agent_bypass()
    test_no_user_agent()
    logger.info("All rate limiting tests completed")
