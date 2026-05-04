import api from './api';


// post 게시글 좋아요 추가
export const like_boards_create = async (data) => {
  const response = await api.post('/likes/boards_create', data);
  return response;
};


// delete 게시글 좋아요 해제
export const like_boards_del = async () => {
  const response = await api.delete('/likes/boards_del');
  return response;
};


// get 게시글 좋아요 개수
export const like_boards_count = async () => {
  const response = await api.get('/likes/boards_count');
  return response;
};


// 댓글 post 추가
export const like_comments_create = async (data) => {
  const response = await api.post('/likes/comments_create', data);
  return response;
};


// 댓글 delete 해제
export const like_comments_del = async () => {
  const response = await api.delete('/likes/comments_del');
  return response;
};


// get 댓글 좋아요 개수
export const like_comments_count = async () => {
  const response = await api.get('/likes/comments_count');
  return response;
};


// post 헬스장 추가
export const like_gyms_create = async (data) => {
  const response = await api.post('/likes/gyms_create', data);
  return response;
};


// delete 헬스장 해제
export const like_gyms_del = async () => {
  const response = await api.delete('/likes/gyms_del');
  return response;
};


// get 헬스장 좋아요 개수
export const like_gyms_count = async () => {
  const response = await api.get('/likes/gyms_count');
  return response;
};


// post 운동기구 추가
export const like_machines_create = async (data) => {
  const response = await api.post('/likes/machines_create', data);
  return response;
};


// delete 운동기구 해제
export const like_machines_del = async () => {
  const response = await api.delete('/likes/machines_del');
  return response;
};


// get 운동기구 좋아요 개수
export const like_machines_count = async () => {
  const response = await api.get('/likes/machines_count');
  return response;
};