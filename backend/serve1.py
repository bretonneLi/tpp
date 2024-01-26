
from importlib import metadata
from typing import List
import os 


from fastapi import FastAPI, UploadFile,File
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from fastapi.middleware.cors import CORSMiddleware #解决跨域问题
PYDANTIC_VERSION = metadata.version("pydantic")
_PYDANTIC_MAJOR_VERSION: int = int(PYDANTIC_VERSION.split(".")[0])

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)
app.add_middleware(
    CORSMiddleware,
     # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
    allow_origins=["*"],
    # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
    allow_credentials=False,
    # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
    allow_methods=["*"],
    # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
    # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
    allow_headers=["*"],
)


@app.post("/uploadfile/")
async def get_upload_file(files: List[UploadFile]):

    return {
        "names":[file.filename for file in files]
    }

@app.post("/pdf_retriever")
async def get_retriever(file:UploadFile=File(...)):
    #保存上传文件
    save_path=f'./pdf_retriever'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    save_file=os.path.join(save_path,file.filename)
    f=open(save_file,'wb')
    data = await file.read()
    f.write(data)
    f.close()

    loader =  PyPDFLoader(f"/home/dubenhao/pdf_retriever/{file.filename}")
    data=loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    splits = text_splitter.split_documents(data)
    vectorstore = FAISS.from_documents(documents=splits, embedding=LlamaCppEmbeddings(model_path="/home/dubenhao/llama/llama-2-7b-chat/ggml-model-q4_k_m.gguf"))
    vectorstore.save_local("/home/dubenhao/vectorstore/db_faiss_serve")
    
    return vectorstore.index_to_docstore_id





if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)