
from typing import  List, Union
import os 


from fastapi import FastAPI, UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from fastapi.middleware.cors import CORSMiddleware #解决跨域问题
from pydantic import BaseModel#Request Body


from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModel,pipeline

import pymysql

main_path="/home/dubenhao"

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

#llm model
llm_name="THUDM/chatglm3-6b"
tokenizer = AutoTokenizer.from_pretrained(llm_name, trust_remote_code=True)
model = AutoModel.from_pretrained(llm_name, trust_remote_code=True)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
llm = HuggingFacePipeline(pipeline=pipe)

#EmbeddingModel
emb_model_name = "BAAI/bge-base-zh-v1.5"
emb_model_kwargs = {'device': 'cpu'}
hf = HuggingFaceBgeEmbeddings(
    model_name=emb_model_name,
    model_kwargs=emb_model_kwargs,
)

# Template
template=""" <指令>根据已知信息，简洁和专业的来回答问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题”，
            不允许在答案中添加编造成分，答案请使用中文。 </指令>\n
            <已知信息>{{context}}</已知信息>\n
            <问题>{{question}}</问题>\n
"""

#connect to MySQL
def get_connection_sql():
    return pymysql.connect(host="localhost", port=3306, user="test_user", password="123456", database="test_data", charset="utf8")

#API
@app.get("/")
def home():
    return {"homepage":"hello, this is a chatbot API build with Llama2-chat-7B and Langchain"}

@app.get("/welcome",tags=["欢迎界面,default message"])
def get_homepage():
    return "default"

@app.get("/database",tags=["初始三个问题"])
def get_mysql():
    conn=get_connection_sql()
    cursor=conn.cursor()
    try:
        cursor.execute("SELECT question ,number_of_question FROM test_question ORDER BY number_of_question DESC;")
        data=cursor.fetchmany(size=3)
    except Exception :
        print("error")
    finally:
        cursor.close()
    return [k for k in dict(data).keys()]

@app.post("/pdf_retriever",tags=["上传文件接口, API for upload pdf file,"])
async def get_retriever(file:UploadFile):
    vectorstore_path=main_path+f"/vectorstore/{file.filename}"
    save_path=main_path+"/pdf_retriever"
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

@app.get("/pdf_retriever/invoke", tags=["语言模型推理接口"])
async def get_response(filename:str,question:str):
    print("Request received")
    conn=get_connection_sql()
    cursor=conn.cursor()
    try:
        cursor.execute(f"INSERT INTO test_question (question,number_of_question) VALUES (\'{question}\',1);")
        conn.commit()
    except Exception :
        print("Write error")
    finally:
        cursor.close()
        conn.close()
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
        os.remove(vectorstore_path+("/index.faiss"))
        os.remove(vectorstore_path+("/index.pkl"))
        os.rmdir(vectorstore_path)
    #删除储存的文件
    filestore_path=main_path+f"/pdf_retriever/{filename}"# path
    if os.path.exists(filestore_path):
        os.remove(filestore_path)
    return {"delete":filename}

#Start  server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)