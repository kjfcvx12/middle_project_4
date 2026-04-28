import axios from "axios";

// 1. Axios 인스턴스 생성 (서버 주소 설정)
const api = axios.create({
  baseURL: "http://127.0.0.1:8081", // 알려주신 백엔드 주소
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default api;
