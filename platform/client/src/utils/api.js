import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
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
