from fastapi import APIRouter
import os 
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from configs.sql_config import get_connection_sql
from configs.model_config import MAIN_PATH
from configs.prompt_config import TEMPLATES
from configs.model_config import LLM_MODELS, EMBEDDING_MODELS
qachain=APIRouter()

@qachain.get("/pdf_retriever/invoke", tags=["语言模型推理接口"])#请求什么时候到达后端
async def get_response(filename:str,modelname:str,embmodelname:str,question:str,templatename:str):
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
    filestore_path=MAIN_PATH+f"/pdf_retriever/{filename}"# path
    vectorstore_path=MAIN_PATH+f"/vectorstore/{filename}"#path
    if os.path.exists(vectorstore_path) and os.path.exists(filestore_path):
        vectorstore=FAISS.load_local(vectorstore_path,embeddings=EMBEDDING_MODELS[embmodelname])
        #construct the qa chain
        retriever = vectorstore.as_retriever(
            search_kwargs={"k": 6}
        )
        qa_chain = RetrievalQA.from_chain_type(
            llm=LLM_MODELS[modelname], 
            retriever=retriever,     
            chain_type_kwargs={
                "prompt":  PromptTemplate(
                template=TEMPLATES[templatename],
                input_variables=["context", "question"]),
            }
        )
        return qa_chain.invoke(question)
    else:
        return "Please upload the target file before request!"
    