from importlib import metadata
from typing import Any, Dict, List, Union
import os 
from datetime import date

from fastapi import FastAPI, UploadFile,File
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from fastapi.middleware.cors import CORSMiddleware #解决跨域问题
from pydantic import BaseModel#Request Body

from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langserve import add_routes
'''
PYDANTIC_VERSION = metadata.version("pydantic")
_PYDANTIC_MAJOR_VERSION: int = int(PYDANTIC_VERSION.split(".")[0])
'''

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
#llm model path
main_path="/home/dubenhao"
model_path=main_path+("/llama/llama-2-7b-chat/ggml-model-q4_k_m.gguf")

llm = LlamaCpp(
    model_path=model_path,
    max_tokens=2048,
    n_gpu_layers=1,
    n_batch=512,
    n_ctx=2048,
    f16_kv=True,

)
template="""[INST]
    Use the following pieces ofcontext to answer the question.If no context provided, answer like a AI assistant. 
    
    {context} 
    Question: {question}
    [/INST]
"""
@app.get("/")
def home():
    return {"homepage":"hello, this is a chatbot API build with Llama2-chat-7B and Langchain"}
@app.post("/uploadfile/")
async def get_upload_file(files: List[UploadFile]):

    return {
        "names":[file.filename for file in files]
    }

@app.post("/pdf_retriever",tags=["上传文件接口, API for upload pdf file,"])
async def get_retriever(file:UploadFile):#fileinfo:file_info, ,uploaded_time:date,embedding_id:int,owner:str
    vectorstore_path=main_path+f"/vectorstore/{file.filename}"
    

    #user_info={"User name":owner, "Embedding_ID":embedding_id,"uploaded_time":uploaded_time}#Information updated
    #Save the upload file
    
    save_path=main_path+"/pdf_retriever" # custom path
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    #save_path_path=save_path+("/")
    #Embedding 
    if not os.path.exists(save_path+"/"+(file.filename)):
        save_file=os.path.join(save_path,file.filename)
        f=open(save_file,'wb')
        data = await file.read()
        f.write(data)
        f.close()
        
        filestore_path=main_path+f"/pdf_retriever/{file.filename}"

        loader =  PyPDFLoader(filestore_path)
        data=loader.load()
        #data[0].metadata.update(user_info) #根据上传的客户信息更改METADATA信息
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        splits = text_splitter.split_documents(data)

        #

        vectorstore = FAISS.from_documents(documents=splits, 
                                           embedding=LlamaCppEmbeddings(model_path=model_path))
        vectorstore.save_local(vectorstore_path)
        #construct the qa chain
      


    #file_upload_time=time.ctime()
    else:
        filestore_path=main_path+f"/pdf_retriever/{file.filename}"
        loader =  PyPDFLoader(filestore_path)
        data=loader.load()
        #data[0].metadata.update(user_info)
        vectorstore=FAISS.load_local(vectorstore_path,embeddings=LlamaCppEmbeddings(model_path=model_path))
        #construct the qa chain


    return  {
                "file_name": file.filename,
                "file_size":file.size,#bytes
                "vector_id":vectorstore.index_to_docstore_id,
                "vector_path":vectorstore_path,
                #"metadata":data[0].metadata,
                #"file_uploaded_time":uploaded_time,
                #"embedding_id":embedding_id,
                #"owner":owner,
                #
                #
                #file_status
            }

@app.get("/pdf_retriever/invoke", tags=["语言模型推理接口"])
async def get_response(filename:str,question:str):
    filestore_path=main_path+f"/pdf_retriever/{filename}"# path
    vectorstore_path=main_path+f"/vectorstore/{filename}"#path
    if os.path.exists(vectorstore_path) and os.path.exists(filestore_path):
        vectorstore=FAISS.load_local(vectorstore_path,embeddings=LlamaCppEmbeddings(model_path=model_path))
        #construct the qa chain
        retriever = vectorstore.as_retriever(
            search_kwargs={"k": 6}
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, 
            retriever=retriever,     
            chain_type_kwargs={
                "prompt":  PromptTemplate(
                template=template,
                input_variables=["context", "question"]),
            }
        )
        return qa_chain.invoke(question)
    else:
        return "Please upload the target file before request!"


    

@app.delete("/pdf_retriever/delete/{filename}",tags=["删除上传文件以及向量的接口"])
async def delete_file(filename:str):
    #删除储存的向量数据
    vectorstore_path=main_path+f"/vectorstore/{filename}"#path

    if os.path.exists(vectorstore_path):
        vectorstore=FAISS.load_local(vectorstore_path,embeddings=LlamaCppEmbeddings(model_path=model_path))
        for id in vectorstore.index_to_docstore_id:
            vectorstore.delete([vectorstore.index_to_docstore_id[0]])
        os.remove(vectorstore_path+("/index.faiss"))
        os.remove(vectorstore_path+("/index.pkl"))
        os.rmdir(vectorstore_path)
    #删除储存的文件
    filestore_path=main_path+f"/pdf_retriever/{filename}"# path

    if os.path.exists(filestore_path):
        os.remove(filestore_path)
    

    return {"delete":filename,"vector_id":vectorstore.index_to_docstore_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)