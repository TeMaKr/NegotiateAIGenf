import re
from ipaddress import IPv4Network, IPv6Network
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from qdrant_client.http.models import Distance

ENVIRONMENT_LITERAL = Literal["LOCAL", "DEVELOPMENT", "PRODUCTION"]


class EnvironmentSettings(BaseModel):
    environment: ENVIRONMENT_LITERAL = "LOCAL"


class RateLimitSettings(BaseModel):
    rate_limit_trusted_proxies_list: list[str] = Field(
        default=[
            "127.0.0.1",
            "::1",
        ]
    )
    rate_limit_allowed_subnet: IPv4Network | IPv6Network | None = Field(default=None)


class CorsSettings(BaseModel):
    allow_origins: list[str] = ["http://localhost:3000"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class CSRFSettings(BaseModel):
    secret: str
    cookie_name: str = "csrf_token"
    cookie_domain: str | None = None
    cookie_secure: bool = True
    cookie_samesite: str = "strict"
    header_name: str = "x-csrf-token"
    exempt_urls: list[re.Pattern] | None = None
    http_only: bool = False


class VectorStore(BaseModel):
    url: str
    api_key: str
    embedding_dim: int = 512
    model: str = "sentence-transformers/distiluse-base-multilingual-cased-v1"
    similarity: Distance = Distance.COSINE


class LLMProvider(BaseModel):
    provider: str = "openai"
    model: str = "gpt-4.1"
    api_key: str


class Redis(BaseModel):
    host: str
    port: int = 6379

    @property
    def dsn(self) -> str:
        return f"redis://{self.host}:{self.port}/0"


class PocketBaseAPI(BaseModel):
    host: str = Field(default="http://localhost:8090")
    token: str = Field(default="...")


class FastAPI(BaseModel):
    host: str = Field(default="http://host.docker.internal:8000")
    token: str = Field(default=...)


class Settings(BaseSettings):
    environment: EnvironmentSettings
    rate_limit: RateLimitSettings
    cors: CorsSettings
    csrf: CSRFSettings
    vector_store: VectorStore
    llm_provider: LLMProvider
    redis: Redis
    pocketbase_api: PocketBaseAPI
    fastapi_api: FastAPI

    model_config = SettingsConfigDict(
        env_prefix="API_",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file=".env",
    )


settings = Settings()
