from typing import Annotated

from fastapi import Header, HTTPException

from settings import settings


async def check_api_token(
    api_token: Annotated[str | None, Header(alias="X-API-Token")] = None,
) -> None:
    """Validates the API token from the request header.

    This function checks the API token provided in the request header against the
    expected value. If the token is missing or invalid, an HTTPException is raised.

    Parameters
    ----------
    api_token: str | None
        The API token provided in the request header. If None, it indicates that no token was
        provided.
    """
    if api_token is None:
        raise HTTPException(status_code=401, detail="API token is required.")

    if api_token != settings.fastapi_api.token:
        raise HTTPException(status_code=403, detail="Invalid API token.")
