import api from './api';


// post 헬스장 즐겨찾기 추가
export const favorite_gyms_create = async (data) => {
  const response = await api.post('/favorites/gyms_create', data);
  return response;
};


// delete 헬스장 즐겨찾기 해제
export const favorite_gyms_del = async () => {
  const response = await api.delete('/favorites/gyms_del');
  return response;
};


// post 운동기구 즐겨찾기 추가
export const favorite_machines_create = async (data) => {
  const response = await api.post('/favorites/machines_create', data);
  return response;
};


// delete 운동기구 즐겨찾기 해제
export const favorite_machines_del = async () => {
  const response = await api.delete('/favorites/machines_del');
  return response;
};


// post 루틴 즐겨찾기 추가
export const favorite_routines_create = async (data) => {
  const response = await api.post('/favorites/routines_create', data);
  return response;
};


// delete 루틴 즐겨찾기 해제
export const favorite_routines_del = async () => {
  const response = await api.delete('/favorites/routines_del');
  return response;
};