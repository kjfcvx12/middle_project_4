import api from './api';


// GET 현재 사용자 확인
export const user_me = async () => {
  const response = await api.get('/users/me');
  return response;
};

// POST 회원가입
export const user_signup = async (data) => {
  const response = await api.post('/users/signup', data);
  return response;
};


// POST 로그인
export const user_login = async (data) => {
  const response = await api.post('/users/login', data);
  return response;
};


// POST 로그아웃
export const user_logout = async () => {
  const response = await api.post('/users/logout');
  return response;
};


// GET 전 유저 조회
export const user_admin_get_all = async () => {
  const response = await api.get('/users/all');
  return response;
};


// GET 잊은 email 조회
export const user_find_email = async ({u_name, phone}) => {
  const response = await api.get('/users/find_email', {params: {u_name, phone}});
  return response;
};


// GET admin 특정 id 사용자 조회
export const user_admin_get_user = async (u_id) => {
  const response = await api.get(`/users/${u_id}`);
  return response;
};


// PUT	현재 id 사용자 수정
export const user_edit = async (data) => {
  const response = await api.put('/users/edit', data);
  return response;
};


// DELETE 현재 id 사용자 삭제
export const user_del = async () => {
  const response = await api.delete('/users/del');
  return response;
};


// 유저 운동기록 조회
export const user_get_logs = async (u_id, page=1) => {
  const response = await api.get(`/users/logs/${u_id}`, {params: {page}});
  return response;
};


// 유저 체육관 즐겨찾기 목록 조회
export const user_get_favorite_gyms = async (u_id) => {
  const response = await api.get(`/users/favorite_gyms/${u_id}`);
  return response;
};


// 유저 운동기구 즐겨찾기 목록 조회
export const user_get_favorite_machines = async (u_id) => {
  const response = await api.get(`/users/favorite_machines/${u_id}`);
  return response;
};


// 유저 루틴 즐겨찾기 목록 조회
export const user_get_favorite_routines = async (u_id) => {
  const response = await api.get(`/users/favorite_routines/${u_id}`);
  return response;
};


// 유저가 좋아요 누른 게시글
export const user_get_like_boards = async (u_id, page) => {
  const response = await api.get(`/users/like_boards/${u_id}`, {params: {page}});
  return response;
};

// 유저가 좋아요 누른 댓글
export const user_get_like_comments = async (u_id, page) => {
  const response = await api.get(`/users/like_comments/${u_id}`, {params: {page}});
  return response;
};


// 유저가 좋아요 누른 운동기구
export const user_get_like_machines = async (u_id, page) => {
  const response = await api.get(`/users/like_machines/${u_id}`, {params: {page}});
  return response;
};


// 유저가 좋아요 누른 체육관
export const user_get_like_gyms = async (u_id, page) => {
  const response = await api.get(`/users/like_gyms/${u_id}`, {params: {page}});
  return response;
};


