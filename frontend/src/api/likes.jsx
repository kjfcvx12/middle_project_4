import api from './api';


// post 게시글 좋아요 토글
export const like_boards_toggle = async (b_id) => {
  const response = await api.post(`/likes/boards/toggle`, null, {
    params: { b_id }
  });
  return response.data;
};


// get 게시글 좋아요 개수
export const like_boards_count = async (b_id) => {
  // params 객체를 통해 b_id를 전달합니다.
  const response = await api.get('/likes/boards_count', {
    params: { b_id } 
  });
  return response.data;
};


// post 댓글 좋아요 토글
export const like_comments_toggle = async (c_id) => {
  const response = await api.post(`/likes/comments/toggle`, null, {
    params: { c_id }
  });
  return response.data;
};


// get 댓글 좋아요 개수
export const like_comments_count = async (c_id) => {
  const response = await api.get('/likes/comments_count', {
    params: { c_id }
  });
  return response;
};


// post 헬스장 좋아요 토글
export const like_gyms_toggle = async (g_id) => {
  const response = await api.post(`/likes/gyms/toggle`, null, {
    params: { g_id }
  });
  return response.data;
};


// get 헬스장 좋아요 개수
export const like_gyms_count = async (g_id) => {
  const response = await api.get('/likes/gyms_count', {
    params: { g_id }
  });
  return response;
};


// post 운동기구 좋아요 토글
export const like_machines_toggle = async (m_id) => {
  const response = await api.post(`/likes/machines/toggle`, null, {
    params: { m_id }
  });
  return response.data;
};


// get 운동기구 좋아요 개수
export const like_machines_count = async (m_id) => {
  const response = await api.get('/likes/machines_count',{
    params: { m_id }
  });
  return response;
};