import json
import logging
from typing import Annotated

from fastapi import APIRouter, Body, Request
from pydantic import BaseModel, Field
from qdrant_client.http.models import FieldCondition, Filter, MatchAny
from starlette import status

# ---------------------------------------------------------------------
# -- ALL ROUTERS IN THIS FILE ARE SUPPOSED TO BE PUBLICLY ACCESSIBLE --
# ---------------------------------------------------------------------

router = APIRouter()
logger = logging.getLogger(__name__)


class SubmissionDataDetail(BaseModel):
    authors: list[str] = []
    topics: list[str] = []


class QuerySubmissionIn(BaseModel):
    question: str = Field(..., min_length=1, max_length=250)
    submission_metadata: dict[str, SubmissionDataDetail] | None = None


class ReferencesOut(BaseModel):
    retriever_id: str
    href: str


class QuerySubmissionOut(BaseModel):
    answer: str
    context: dict[str, list[str]] = {}
    references: list[ReferencesOut] = []


@router.post(
    path="/query-submission",
    response_model=QuerySubmissionOut,
    status_code=status.HTTP_200_OK,
)
async def query_submission(
    query: Annotated[QuerySubmissionIn, Body(..., description="Question to submit")],
    Request: Request,
) -> QuerySubmissionOut:
    query_submissions_tool = Request.app.state.query_submission_tool

    if query.submission_metadata:
        retriever_ids = list(query.submission_metadata.keys())

        doc_id_filter = Filter(
            must=[
                FieldCondition(
                    key="metadata.retriever_id",
                    match=MatchAny(any=retriever_ids),
                )
            ]
        )

        submission_metadata_dict = {
            key: value.model_dump()  # Convert Pydantic object to dict
            for key, value in query.submission_metadata.items()
        }

        response = await query_submissions_tool.ainvoke(
            {
                "question": query.question,
                "filter": doc_id_filter,
                "submission_metadata": submission_metadata_dict,
            }
        )
    else:
        response = await query_submissions_tool.ainvoke(
            {
                "question": query.question,
                "submission_metadata": query.submission_metadata,
            }
        )

    answer = response["answer"]
    context: dict[str, list[str]] = {}
    for doc in response["context"]:
        id = context.get(doc.metadata["retriever_id"])
        if id is None:
            context[doc.metadata["retriever_id"]] = []
        doc_content_processed = doc.page_content.split("|")
        if len(doc_content_processed) == 2:
            actual_text = doc_content_processed[1].strip()
        else:
            actual_text = doc.page_content
        context[doc.metadata["retriever_id"]].append(actual_text)
    references = []
    seen = set()
    for doc in response["context"]:
        key = (doc.metadata["retriever_id"], doc.metadata["href"])
        if key not in seen:
            seen.add(key)
            references.append(
                ReferencesOut(
                    retriever_id=doc.metadata["retriever_id"],
                    href=doc.metadata["href"],
                )
            )
    return QuerySubmissionOut(
        answer=answer,
        context=context,
        references=references,
    )


class SubmissionExtract(BaseModel):
    author: list[str]
    text: str


class SummaryKeyElementIn(BaseModel):
    key_element: str = Field(..., min_length=1, max_length=85)
    submission_extracts: list[SubmissionExtract]


class SummaryKeyElementOut(BaseModel):
    summary: str


@router.post(
    path="/summarize-key-element",
    response_model=SummaryKeyElementOut,
    status_code=status.HTTP_200_OK,
)
async def summarize_key_element(
    query: Annotated[
        SummaryKeyElementIn,
        Body(..., description="Key element and submission extracts"),
    ],
    Request: Request,
) -> SummaryKeyElementOut:
    summarize_submissions_tool = Request.app.state.summarize_submissions_tool

    # Convert submission_extracts to JSON string for debugging
    try:
        submission_extracts_json = json.dumps(
            [extract.model_dump() for extract in query.submission_extracts],
            indent=2,
            ensure_ascii=False,  # This helps with special characters
        )
        logger.info(f"Submission extracts JSON:\n{submission_extracts_json}")
    except Exception as e:
        logger.error(f"Error serializing submission extracts to JSON: {e}")

    summary = await summarize_submissions_tool(
        submission_extracts=[
            extract.model_dump() for extract in query.submission_extracts
        ],
        key_element=query.key_element,
        llm=Request.app.state.llm,
    )

    return SummaryKeyElementOut(summary=summary)
