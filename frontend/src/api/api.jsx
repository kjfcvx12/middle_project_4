import axios from 'axios';

// 1. Axios 인스턴스 생성
const api = axios.create({
  baseURL: 'http://localhost:8081', // 백엔드 주소
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true // ⭐ 중요: 쿠키를 자동으로 주고받게 함
});

// 인터셉터는 이제 '토큰 삽입' 용도가 아니라, 
// 에러 공통 처리(예: 401 발생 시 로그아웃) 용도로만 사용하게 됩니다.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // 여기서 필요하다면 전역 로그아웃 처리를 할 수 있습니다.
      console.warn("인증 세션이 없거나 만료되었습니다.");
    }
    return Promise.reject(error);
  }
);

export default api;
