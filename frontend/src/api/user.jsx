import api from './api';


export const user_login = async (credentials) => {
  const response = await api.post('/users/login', credentials);
  return response;
};
