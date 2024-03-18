import aioxs from 'axios';
import {REACT_APP_WP_API_BASE} from "../global-config";

const Request = aioxs.create({
    baseURL: REACT_APP_WP_API_BASE, //"http://localhost:8089/wordpress/?rest_route=",
    timeout: 5000
});


// request interceptor
Request.interceptors.request.use((config) => {
    return config
}, function (error) {
    //todo when request error
    return Promise.reject(error)
}
)

 
// response interceptor
Request.interceptors.response.use((response) => {
    return response
}, function (error) {
    //todo if error encountered when response comes back
    return Promise.reject(error)
}
)

export default Request;