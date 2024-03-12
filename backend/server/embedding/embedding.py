import os 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from fastapi import APIRouter,UploadFile
from configs.model_config import MAIN_PATH,EMBEDDING_MODELS


embedding= APIRouter()

@embedding.post("/pdf_retriever",tags=["上传文件接口, API for upload pdf file,"])
async def get_retriever(file:UploadFile,embmodelname:str):#fileinfo:file_info, ,uploaded_time:date,embedding_id:int,owner:str
    vectorstore_path=MAIN_PATH+f"/vectorstore/{file.filename}"
    

    #user_info={"User name":owner, "Embedding_ID":embedding_id,"uploaded_time":uploaded_time}#Information updated
    #Save the upload file
    
    save_path=MAIN_PATH+"/pdf_retriever" # custom path
    if not os.path.exists(save_path):
        os.mkdir(save_path)


    #Embedding 
    if not os.path.exists(save_path+"/"+(file.filename)):
        save_file=os.path.join(save_path,file.filename)
        f=open(save_file,'wb')
        data = await file.read()
        f.write(data)
        f.close()
        filestore_path=MAIN_PATH+f"/pdf_retriever/{file.filename}"
        loader =  PyPDFLoader(filestore_path)
        data=loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        splits = text_splitter.split_documents(data)
        vectorstore = FAISS.from_documents(documents=splits, 
                                           embedding=EMBEDDING_MODELS[embmodelname])
        vectorstore.save_local(vectorstore_path)
    else:
        vectorstore=FAISS.load_local(vectorstore_path,embeddings=EMBEDDING_MODELS[embmodelname])
    return  {
                "file_name": file.filename,
                "file_size":file.size,#bytes
                "vector_id":vectorstore.index_to_docstore_id,
                "vector_path":vectorstore_path,
            }

@embedding.delete("/pdf_retriever/delete/{filename}",tags=["删除上传文件以及向量的接口"])
async def delete_file(filename:str):
    #删除储存的向量数据
    vectorstore_path=MAIN_PATH+f"/vectorstore/{filename}"#path
    if os.path.exists(vectorstore_path):

        os.remove(vectorstore_path+("/index.faiss"))
        os.remove(vectorstore_path+("/index.pkl"))
        os.rmdir(vectorstore_path)
    #删除储存的文件
    filestore_path=MAIN_PATH+f"/pdf_retriever/{filename}"# path
    if os.path.exists(filestore_path):
        os.remove(filestore_path)
    return {"delete":filename}
