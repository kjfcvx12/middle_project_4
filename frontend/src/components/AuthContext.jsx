import { createContext, useContext, useEffect, useState } from "react";
import { user_login, user_logout, user_me, user_signup } from "./../api/user";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);


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
        setIsLoggedIn(false);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };
    initAuth();
  }, []);


  const login = async (data) => {
    try {
      const response = await user_login(data);
      setUser(response.data);
      setIsLoggedIn(true);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || "로그인 실패",
      };
    }
  };


  const logout = async () => {
    try {
      await user_logout();
    } catch (error) {
      console.error("로그아웃 요청 실패:", error);
    } finally {
      setIsLoggedIn(false);
      setUser(null);
    }
  };


  const signup = async (data) => {
    try {
      await user_signup(data);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || "회원가입 실패",
      };
    }
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, setIsLoggedIn, user, login, logout, signup, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
