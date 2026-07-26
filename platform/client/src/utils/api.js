import axios from 'axios';
import { API_BASE_URL } from '../config/env';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true
});

// Response interceptor to unwrap EnvelopeRoute payloads
api.interceptors.response.use(
  (response) => {
    // If the response is wrapped by the EnvelopeRoute middleware, unwrap the data
    if (response.data && typeof response.data === 'object' && response.data.success === true && 'data' in response.data) {
      response.data = response.data.data;
    }
    return response;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
