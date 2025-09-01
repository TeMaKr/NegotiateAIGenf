from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from settings import settings


def get_llm() -> BaseChatModel:
    """Initialize the chat model with the specified provider and model.

    Returns
    -------
    BaseChatModel
        The initialized chat model.
    """
    return init_chat_model(
        model=settings.llm_provider.model,
        model_provider=settings.llm_provider.provider,
    )
