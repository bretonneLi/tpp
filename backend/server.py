from importlib import metadata
from typing import Any, Dict, List, Union
import os 
from datetime import date

from fastapi import FastAPI, UploadFile,File
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import LlamaCppEmbeddings, HuggingFaceInstructEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from fastapi.middleware.cors import CORSMiddleware #解决跨域问题
from pydantic import BaseModel#Request Body

from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langserve import add_routes

import pymysql

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
#EmbeddingModel
model_name = "hkunlp/instructor-large"
model_kwargs = {'device': 'cpu'}

hf = HuggingFaceInstructEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
)


template="""[INST]
    Use the following pieces ofcontext to answer the question.If no context provided, answer like a AI assistant. 
    
    {context} 
    Question: {question}
    [/INST]
"""

#connect to MySQL







#API
@app.get("/")
def home():
    return {"homepage":"hello, this is a chatbot API build with Llama2-chat-7B and Langchain"}

@app.get("/welcome",tags=["欢迎界面，default message"])
def get_homepage():
    return "default"

@app.get("/database",tags=["初始三个问题"])
def get_mysql():
    conn=pymysql.connect(host="localhost", port=3306, user="test_user", password="123456", database="test_data", charset="utf8")
    cursor=conn.cursor()
    try:
        cursor.execute("SELECT question ,number_of_question FROM test_question ORDER BY number_of_question DESC;")
        data=cursor.fetchmany(size=3)
    except Exception :
        print("error")
    finally:
        cursor.close()
    return dict(data)

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
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        splits = text_splitter.split_documents(data)
        vectorstore = FAISS.from_documents(documents=splits, 
                                           embedding=hf)
        vectorstore.save_local(vectorstore_path)
    else:
        vectorstore=FAISS.load_local(vectorstore_path,embeddings=hf)
    return  {
                "file_name": file.filename,
                "file_size":file.size,#bytes
                "vector_id":vectorstore.index_to_docstore_id,
                "vector_path":vectorstore_path,
            }

@app.get("/pdf_retriever/invoke", tags=["语言模型推理接口"])#请求什么时候到达后端
async def get_response(filename:str,question:str):
    print("Request received")
    filestore_path=main_path+f"/pdf_retriever/{filename}"# path
    vectorstore_path=main_path+f"/vectorstore/{filename}"#path
    if os.path.exists(vectorstore_path) and os.path.exists(filestore_path):
        vectorstore=FAISS.load_local(vectorstore_path,embeddings=hf)
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
        vectorstore=FAISS.load_local(vectorstore_path,embeddings=hf)
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