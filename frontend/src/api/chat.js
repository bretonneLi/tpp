import axios from "axios";
import Request from "./request";
import {REACT_APP_TPP_BACK_BASE} from "../global-config";

export function retriver(question, modelname){
    let filename='tingyimiao.pdf';
    // 使用模板字符串将参数拼接在 URL 上
    return axios.get(REACT_APP_TPP_BACK_BASE+`pdf_retriever/invoke?question=${question}&filename=${filename}&modelname=${modelname}`);
}

// 机器人初始加载欢迎语
export function chatInit(){
    return axios.get(REACT_APP_TPP_BACK_BASE+ `database`);
}

 // get current LLM
 export function getCurrentLLM(){
    return Request({
      url:"/llm/v1/target",
      method: 'GET',
      params: {
      }
    })
  }