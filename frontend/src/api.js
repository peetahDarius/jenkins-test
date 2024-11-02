import axios from 'axios';
import { ACCESS_TOKEN, REFRESH_TOKEN } from "./apiConstants";

// Create an Axios instance
const api = axios.create({
    baseURL: process.env.REACT_APP_BACKEND_URL
});

// Request interceptor to add token to headers
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
            config.headers['Content-Type'] = 'application/json';
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// // Response interceptor to handle unauthorized errors
// api.interceptors.response.use(
//     (response) => response,
//     async (error) => {
//         const { response } = error;
//         if (response && response.status === 401) {
//             // Clear local storage and redirect to login page
//             localStorage.clear();
//             window.location.href = '/login'; // Redirect to login page
//         }
//         return Promise.reject(error);
//     }
// );

export default api;