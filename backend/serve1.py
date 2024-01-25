
from importlib import metadata
from typing import List




from fastapi import FastAPI, UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.document_loaders import PyPDFLoader
PYDANTIC_VERSION = metadata.version("pydantic")
_PYDANTIC_MAJOR_VERSION: int = int(PYDANTIC_VERSION.split(".")[0])

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)


@app.post("/uploadfile/")
async def get_upload_file(files: List[UploadFile]):

    return {
        "names":[file.filename for file in files]
    }

@app.post("/pdf_retriever")
async def get_retriever(file:UploadFile):
    loader =  PyPDFLoader(file.filename)
    data=loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10, chunk_overlap=0)
    splits = text_splitter.split_documents(data)
    vectorstore = FAISS.from_documents(documents=splits, embedding=LlamaCppEmbeddings(model_path="/home/dubenhao/llama/llama-2-7b-chat/ggml-model-q4_k_m.gguf"))
    retriever=vectorstore.as_retriever()
    return {"retriever":"ok"}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)