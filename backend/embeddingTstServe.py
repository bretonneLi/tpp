from importlib import metadata
from typing import List

from fastapi.middleware.cors import CORSMiddleware #解决跨域问题

from fastapi import FastAPI,Form, UploadFile

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

# emb_id, owner, uploaded_time
@app.post("/embedding/pdf_retriever/")
async def create_upload_file(file: UploadFile, owner:str=Form(...),uploadedTime:str=Form(...),embId:str=Form(...)):
    return {"file_name": file.filename, "owner": owner, 'embId': embId}

@app.get("/qachain/pdf_retriever/invoke", tags=["语言模型推理接口"])
async def get_response(filename:str,question:str,modelname:str):
    return {"result": question, "query": question}

@app.get("/welcome/database", tags=["对话初始加载欢迎语"])
async def chat_init():
    return ["Weclome.","I am TPP Agent and I only answer in English and French","Select a topic in the below list or ask me directly your question."]

@app.get("/getconfigs/llmnames", tags=["获取模型list"])
async def llm_list():
    return ['llma2', 'chatglm3-6b', 'chatGPT4']

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)