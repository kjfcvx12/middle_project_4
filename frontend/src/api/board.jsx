import api from "./api";

// 게시글 목록
export const getBoards = async (page = 1, size = 10) => {
  const response = await api.get(`/boards?page=${page}&size=${size}`);
  return response.data;
};

// 게시글 상세
export const getBoardDetail = async (b_id) => {
  const response = await api.get(`/boards/${b_id}`);
  return response.data;
};

// 게시글 작성
export const createBoard = async (boardData) => {
  const response = await api.post(`/boards/create`, boardData);
  return response.data;
};

// 게시글 수정
export const updateBoard = async (b_id, boardData) => {
  const response = await api.put(`/boards/${b_id}`, boardData);
  return response.data;
};

// 게시글 삭제
export const deleteBoard = async (b_id) => {
  const response = await api.delete(`/boards/${b_id}`);
  return response.data;
};

// 댓글 목록
export const getComments = async (b_id) => {
  const response = await api.get(`/boards/${b_id}/comments`);
  return response.data;
};

// 댓글 작성
export const createComment = async (b_id, commentData) => {
  const response = await api.post(`/boards/${b_id}/comments`, commentData);
  return response.data;
};

// 댓글 수정
export const updateComment = async (b_id, c_id, commentData) => {
  const response = await api.put(
    `/boards/${b_id}/comments/${c_id}`,
    commentData,
  );
  return response.data;
};

// 댓글 삭제
export const deleteComment = async (b_id, c_id) => {
  const response = await api.delete(`/boards/${b_id}/comments/${c_id}`);
  return response.data;
};
