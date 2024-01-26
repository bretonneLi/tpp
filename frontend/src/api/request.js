import aioxs from 'axios';

const Request = aioxs.create({
    baseURL: "http://localhost:8088/",
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