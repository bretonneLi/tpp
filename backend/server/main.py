from fastapi import FastAPI
from chain.qachain import qachain
from embedding.embedding import embedding
from configs.get_configs import getConfigs
from configs.welcome import welcome
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"homepage":"hello, this is a chatbot API build with Llama2-chat-7B and Langchain"}
app.include_router(qachain,prefix="/qachain")
app.include_router(embedding,prefix="/embedding")
app.include_router(getConfigs,prefix="/getconfigs")
app.include_router(welcome,prefix="/welcome")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost",port=8000)