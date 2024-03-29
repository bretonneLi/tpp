from fastapi import APIRouter
from configs.model_config import LLM_MODELS, EMBEDDING_MODELS
from configs.prompt_config import TEMPLATES
getConfigs = APIRouter()

@getConfigs.get("/llmnames",tags=["Getting the names of LLMs"])
def get_llm_list():
    llm_name=LLM_MODELS.keys()
    return list(llm_name)

@getConfigs.get("/embeddingnames",tags=["Getting the names of Embedding Models"])
def get_emb_list():
    emb_name=EMBEDDING_MODELS.keys()
    return list(emb_name)

@getConfigs.get("/templatenames",tags=["Getting the names of Templates"])
def get_templat_name():
    templat_name=TEMPLATES.keys()
    return list(templat_name)

