import axios from 'axios'

// const instance = axios.create({
//     baseURL: 'http://localhost:5000',
//     headers: {
//         'Content-Type': 'application/json',
//     },
//     timeout: 10000,
// })

const instance = axios.create({
    baseURL: 'http://34.132.132.120:8080',
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10000,
})


instance.interceptors.request.use(config => {    
    return config
}, err => {
    return Promise.reject(err)
});


instance.interceptors.response.use(res => {
    return res.data
}, err => {
    return Promise.reject(err)
});

export default instance