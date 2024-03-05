import axios from "axios";
import Request from "./request";

// upload embedding file
export function uploadFile(url, file, recordId){
    let formData = new FormData(); 
    formData.append('file', file); 
    formData.append('owner', 'admin');
    // get current time
    let currentTime = new Date(); // 创建一个表示当前时间的Date对象
    // 格式化为指定的字符串形式（yyyy-MM-dd HH:mm:ss）
    let formattedTime = currentTime.getFullYear() + '-' 
    + (currentTime.getMonth()+1).toString().padStart(2, '0') + '-' 
    + currentTime.getDate().toString().padStart(2, '0')+ ' '
    + currentTime.getHours().toString().padStart(2, '0')+':'
    + currentTime.getMinutes().toString().padStart(2, '0')+':'
    + currentTime.getSeconds().toString().padStart(2, '0');
    
    formData.append('uploadedTime', formattedTime);
    formData.append('embId', recordId);
    return axios.post(process.env.REACT_APP_TPP_BACK_BASE+url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data' 
      }
    });
}

// add embedding record
export function addEmbeddingRecord(data){
  return Request({
    url:"/embedding/v1/save",
    method: 'POST',
    data: data
  })
}

// add embedding record
export function updateEmbeddingRecord(data){
  return Request({
     url:"/embedding/v1/update",
     method: 'POST',
     data: data
   })
 }

 // load all embedding records
export function getEmbeddingRecords(){
  return Request({
    url:"/embedding/v1/list",
    method: 'GET',
    params: {
      'owner': 'admin'
    }
  })
}
