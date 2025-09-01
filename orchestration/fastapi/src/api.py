import os
from contextlib import asynccontextmanager
from typing import Sequence

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ratelimit import RateLimitMiddleware, Rule

from routers import ai_tools, submissions
from security import ratelimit
from settings import settings
from tools import llm_provider
from tools.query_submissions import build_query_submissions_tool
from tools.summarize_submissions import summarize
from vector_database.session import inc_vector_store

API_PREFIX = "/api"


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.environ["OPENAI_API_KEY"] = settings.llm_provider.api_key
    llm = llm_provider.get_llm()
    query_submissions_tool = build_query_submissions_tool(llm=llm)

    app.state.llm = llm
    app.state.inc_vector_store = inc_vector_store
    app.state.query_submission_tool = query_submissions_tool
    app.state.summarize_submissions_tool = summarize
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/api/ping")
def pong():
    return {"ping": "pong!"}


# Set rate limiting rules here
rules: dict[str, Sequence[Rule]] = {
    rf"^{API_PREFIX}/query-submission$": [Rule(minute=20, second=5)],
    rf"^{API_PREFIX}/summarize-key-element$": [Rule(minute=20, second=5)],
}

app.add_middleware(
    RateLimitMiddleware,
    authenticate=ratelimit.auth_method,
    backend=ratelimit.redis_backend,
    config=rules,
)

app.include_router(ai_tools.router, prefix=API_PREFIX, tags=["AI Tools"])

app.include_router(submissions.router, prefix=API_PREFIX, tags=["Submissions"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allow_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)
