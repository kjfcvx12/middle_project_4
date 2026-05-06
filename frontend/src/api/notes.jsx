import api from './api';


// GET 본인 보낸쪽지함 조회
export const note_outbox = async () => {
  const response = await api.get('/notes/outbox');
  return response;
};


// GET 본인 받은쪽지함 조회
export const note_inbox = async () => {
  const response = await api.get('/notes/inbox');
  return response;
};


// GET 쪽지 상세
export const note_detail = async (n_id) => {
  const response = await api.get(`/notes/${n_id}`);
  return response;
};


// POST 쪽지 생성
export const note_create = async (data) => {
  const response = await api.post('/notes/create', data);
  return response;
};


// PUT 본인 보낸쪽지함 삭제 변경
export const note_send_del = async (n_id) => {
  const response = await api.put(`/notes/outbox/${n_id}`);
  return response;
};


// PUT	현재 id 사용자 수정
export const note_rece_del = async (n_id) => {
  const response = await api.put(`/notes/inbox/${n_id}`);
  return response;
};


// DELETE 현재 id 사용자 삭제
export const note_del = async () => {
  const response = await api.delete('/notes/del');
  return response;
};
