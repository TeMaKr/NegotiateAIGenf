from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request
from pydantic import AnyHttpUrl, BaseModel
from qdrant_client.models import FieldCondition, Filter, MatchValue
from starlette import status

from security.api_token import check_api_token
from tasks import embed, synchronize

router = APIRouter(dependencies=[Depends(check_api_token)])


class SynchronizeSubmissionsIn(BaseModel):
    base_url: AnyHttpUrl


class SynchronizationSubmissionsOut(BaseModel):
    message: str
    task_id: str


@router.post(
    "/synchronize-submission",
    status_code=status.HTTP_201_CREATED,
    response_model=SynchronizationSubmissionsOut,
)
async def synchronize_submissions(
    session: Annotated[
        SynchronizeSubmissionsIn, Body(..., description="Base Url of Subsession 5")
    ],
) -> SynchronizationSubmissionsOut:
    """
    Spawn a background task to synchronize the submissions with the UNEP Website from session 5.2.
    """
    task = synchronize.delay(base_url=session.base_url)
    return SynchronizationSubmissionsOut(
        message="Synchronization task started successfully.",
        task_id=task.id,
    )


class IncDocumentIn(BaseModel):
    submission_id: str
    file_path: str
    retriever_id: str
    href: str
    key_elements: dict[str, list[str]] | None = None
    session: str


class IncDocumentOut(BaseModel):
    message: str
    task_id: str


@router.post(
    path="/process-submission",
    status_code=201,
)
async def inc_document(
    document: Annotated[
        IncDocumentIn, Body(..., description="Document to process and upsert")
    ],
) -> IncDocumentOut:
    """
    Endpoint to process and upsert a document into the 'inc' vector store.
    """
    task = embed.delay(
        file_path=document.file_path,
        submission_id=document.submission_id,
        retriever_id=document.retriever_id,
        href=document.href,
        key_elements=document.key_elements,
        session=document.session,
    )
    return IncDocumentOut(
        message="Document processing and embedding task started successfully.",
        task_id=task.id,
    )


class DeleteSubmissionVectorIn(BaseModel):
    retriever_id: str


@router.delete(
    path="/delete-submission-vector",
)
async def delete_submission_vector(
    retriever_id: Annotated[
        DeleteSubmissionVectorIn, Body(..., description="The submission id")
    ],
    Request: Request,
) -> None:
    inc_vector_store = Request.app.state.inc_vector_store
    delete_filter = Filter(
        must=[
            FieldCondition(
                key="metadata.retriever_id",
                match=MatchValue(value=retriever_id.retriever_id),
            )
        ]
    )
    inc_vector_store.client.delete(collection_name="inc", points_selector=delete_filter)
