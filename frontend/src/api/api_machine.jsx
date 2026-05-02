import api from './api';

// 목록 조회
export const machines_read = () => {
  return api.get('/machines');
};

// 상세 조회
export const machines_read_detail = (m_id) => {
  return api.get(`/machines/${m_id}`);
};

// 생성 (admin)
export const machines_create = (data) => {
  return api.post('/machines', data);
};

// 수정 (manager)
export const machines_update = (m_id, data) => {
  return api.put(`/machines/${m_id}`, data);
};

// 삭제 (admin)
export const machines_delete = (m_id) => {
  return api.delete(`/machines/${m_id}`);
};