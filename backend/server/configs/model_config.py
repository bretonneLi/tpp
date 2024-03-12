import os
from configs.models import (get_llm_model,
                            get_HFBgeEmbedding_model,
                            get_HFInstructorEmbedding_model,
                            get_llama_cpp)

MAIN_PATH="/home/dubenhao"

MODEL_PATH = {
    "embed_model": {
        "instructor-large":"hkunlp/instructor-large",
        "bge-base-zh-v1.5": "BAAI/bge-base-zh-v1.5",
    },

    "llm_model": {
        "chatglm3-6b": "THUDM/chatglm3-6b",
        "Llama-2-7b-chat-hf": "meta-llama/Llama-2-7b-chat-hf",
        "Llama.cpp":"/home/dubenhao/llama/llama-2-7b-chat/ggml-model-q4_k_m.gguf"
    }
}

EMBEDDING_MODELS = {"instructor-large":get_HFInstructorEmbedding_model(MODEL_PATH["embed_model"]["instructor-large"]),
                    "bge-base-zh-v1.5":get_HFBgeEmbedding_model(MODEL_PATH["embed_model"]["bge-base-zh-v1.5"])
                    }

LLM_MODELS = {"chatglm3-6b":get_llm_model(MODEL_PATH["llm_model"]["chatglm3-6b"]), 
              #"Llama-2-7b-chat-hf":get_llm_model(MODEL_PATH["llm_model"]["Llama-2-7b-chat-hf"]),
              "Llama.cpp":get_llama_cpp(MODEL_PATH["llm_model"]["Llama.cpp"])

            }


if __name__=="__main__":
    print(MODEL_PATH["embed_model"]["instructor-large"])
#把模型列表传给前端







