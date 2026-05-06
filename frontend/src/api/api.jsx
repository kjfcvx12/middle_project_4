import axios from 'axios';

// 1. Axios 인스턴스 생성
const api = axios.create({
  baseURL: 'http://localhost:8081',
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true // 그대로 유지 (다른 API 영향 가능)
});


// 2. 🔥 JWT만 추가하는 요청 인터셉터 "추가"
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);


// 3. 기존 응답 인터셉터 그대로 유지
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn("인증 세션이 없거나 만료되었습니다.");
    }
    return Promise.reject(error);
  }
);

export default api;