from langchain_community.embeddings import HuggingFaceBgeEmbeddings,HuggingFaceInstructEmbeddings
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModel, pipeline
from langchain_community.llms import LlamaCpp
#modelpath could be a local path or a file path of HuggingFace
def get_llm_model(modelpath:str):
    tokenizer = AutoTokenizer.from_pretrained(modelpath, trust_remote_code=True)
    model = AutoModel.from_pretrained(modelpath, trust_remote_code=True)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    llm = HuggingFacePipeline(pipeline=pipe)
    return llm
#
def get_llama_cpp(modelpath:str):
    llm = LlamaCpp(
        model_path=modelpath,
        max_tokens=2048,
        n_gpu_layers=1,
        n_batch=512,
        n_ctx=2048,
        f16_kv=True,
    )
    return llm


def get_HFBgeEmbedding_model(modelpath:str,emb_model_kwargs = {'device': 'cpu'}):
    hf = HuggingFaceBgeEmbeddings(
        model_name=modelpath,
        model_kwargs=emb_model_kwargs,
    )
    return hf

def get_HFInstructorEmbedding_model(modelpath:str,emb_model_kwargs = {'device': 'cpu'}):
    hf = HuggingFaceInstructEmbeddings(
        model_name=modelpath,
        model_kwargs=emb_model_kwargs,
    )
    return hf

if __name__ =="__main__":
     get_llm_model("meta-llama/Llama-2-7b-chat-hf")