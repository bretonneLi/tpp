import axios from "axios";

// upload embedding file
export function uploadFile(url, file){
    let formData = new FormData(); 
    formData.append('file', file); 
  
    return axios.post('http://localhost:8000'+url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data' 
      }
    });
}