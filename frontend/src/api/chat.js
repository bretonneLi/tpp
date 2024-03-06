import axios from "axios";
import Request from "./request";

export function retriver(question){
    let filename='tingyimiao.pdf';
    // 使用模板字符串将参数拼接在 URL 上
    return axios.get(process.env.REACT_APP_TPP_BACK_BASE+`pdf_retriever/invoke?question=${question}&filename=${filename}`);
}

// 机器人初始加载欢迎语
export function chatInit(){
    return axios.get(process.env.REACT_APP_TPP_BACK_BASE+ `database`);
}