import logging
import os

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate
from qdrant_client.models import FieldCondition, Filter, MatchValue

from settings import settings
from vector_database.session import inc_vector_store

os.environ["OPENAI_API_KEY"] = settings.llm_provider.api_key


logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


template = """
You are an expert on submissions to the UN negotiations on the INC Plastics Treaty. You are to provide sentences from the parts of submission for each of these Key Elements of {article} of the treaty.

Key Elements:
{key_elements}

Submission Parts:
{context}

Only give the answer for the Key Element: {search_key_element}. Separate with semicolon if different passages. Do not include any other text or explanation. If there are no relevant sentences, return an empty string."""


def extract_relevant_sentences(
    search_key_element: str,
    article: str,
    key_elements: list[str],
    llm: BaseChatModel,
    filter: Filter | None = None,
) -> str:
    retrieved_docs = inc_vector_store.similarity_search(
        search_key_element,
        k=5,
        filter=filter,
    )

    docs_content = ""

    for doc in retrieved_docs:
        temp_doc_context = (
            f"Reference ID {doc.metadata['retriever_id']}: {doc.page_content} \n\n"
        )
        docs_content += temp_doc_context

    prompt = PromptTemplate.from_template(template)

    messages = prompt.invoke(
        {
            "key_element": search_key_element,
            "article": article,
            "key_elements": ";".join(key_elements),
            "search_key_element": search_key_element,
            "context": docs_content,
        }
    )

    response = llm.invoke(messages)
    response_content = response.content

    return str(response_content)
