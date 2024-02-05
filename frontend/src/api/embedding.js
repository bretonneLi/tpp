import axios from "axios";
import Request from "./request";

// upload embedding file
export function uploadFile(url, file, recordId){
    let formData = new FormData(); 
    formData.append('file', file); 
    formData.append('owner', 'admin');
    formData.append('uploaded_time', '2024-01-01 10:00:00')
    formData.append('emb_fild_id', recordId);
    return axios.post('http://localhost:8000'+url, formData, {
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

export function getEmbeddingRecords(){
  return Request({
    url:"/embedding/v1/list",
    method: 'GET',
    params: {
      'owner': 'admin'
    }
  })
}