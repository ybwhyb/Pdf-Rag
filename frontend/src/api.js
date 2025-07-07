import axios from 'axios';

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:4000',
  withCredentials: true,
});

export const uploadFile = (file, onUploadProgress) => {
  const formData = new FormData();
  formData.append('file', file);
  return API.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress,
  });
};
