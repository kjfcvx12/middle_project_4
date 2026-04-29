import { createContext, useState, useContext, useEffect } from 'react';
import { user_login, user_me, user_signup, user_logout } from './../api/user';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // 1. 앱 접속 시 세션 확인 (Silent Refresh 역할)
  useEffect(() => {
    const initAuth = async () => {
      try {
        // 백엔드 쿠키가 있으면 유저 정보가 오고, 없으면 에러가 납니다.
        const response = await user_me(); 
        if (response.data) {
          setUser(response.data);
          setIsLoggedIn(true);
        }
      } catch (error) {
        // 인증되지 않은 사용자 (자연스러운 상태)
        setIsLoggedIn(false);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };
    initAuth();
  }, []);

  // 2. 로그인 로직
  const login = async (data) => {
    try {
      const response = await user_login(data);
      // 백엔드에서 return db_user를 해주므로 response.data가 곧 유저 정보입니다.
      setUser(response.data);
      setIsLoggedIn(true);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || "로그인 실패" };
    }
  };

  // 3. 로그아웃 로직
  const logout = async () => {
    try {
      await user_logout(); // 백엔드 쿠키 삭제 요청
    } catch (error) {
      console.error("로그아웃 요청 실패:", error);
    } finally {
      // 서버 응답과 상관없이 프론트 상태 초기화
      setIsLoggedIn(false);
      setUser(null);
    }
  };

  // 4. 회원가입 로직
  const signup = async (data) => {
    try {
      await user_signup(data);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || "회원가입 실패" };
    }
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, user, login, logout, signup, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
