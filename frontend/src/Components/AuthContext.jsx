import { createContext, useState, useContext } from 'react';
import { user_login } from '../api/user';

const AuthContext = createContext(null);


export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  // 2. 로그인 로직 연동
  const login = async (credentials) => {
    try {
      const response = await user_login(credentials)
      // 서버에서 토큰을 준다면 로컬 스토리지에 저장
      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
      }
      setIsLoggedIn(true);
      setUser(response.data.user);
      return { success: true };
    } catch (error) {
      console.error("로그인 실패:", error.response?.data || error.message);
      return { success: false, error: error.response?.data };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    setUser(null);
  };

  const signup = async (userData) => {
    try {
      await api.post('/users/signup', userData);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data };
    }
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, user, login, logout, signup }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
