import api from './api';


// post 헬스장 즐겨찾기 토글
export const favorite_gyms_toggle = async (g_id) => {
  const response = await api.post(`/favorites/gyms/toggle`, null, {
    params: { g_id }
  });
  return response.data;
};


// post 운동기구 즐겨찾기 토글
export const favorite_machines_toggle = async (m_id) => {
  const response = await api.post(`/favorites/machines/toggle`, null, {
    params: { m_id }
  });
  return response.data;
};


// post 루틴 즐겨찾기 토글
export const favorite_routines_toggle = async (r_id) => {
  const response = await api.post(`/favorites/routines/toggle`, null, {
    params: { r_id }
  });
  return response.data;
};

