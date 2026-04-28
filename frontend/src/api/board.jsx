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
export const createBoard = async (u_id, boardData) => {
  const response = await api.post(`/boards/create?u_id=${u_id}`, boardData);
  return response.data;
};

// 댓글 목록
export const getComments = async (b_id) => {
  const response = await api.get(`/boards/${b_id}/comments`);
  return response.data;
};

// 댓글 작성
export const createComment = async (b_id, u_id, commentData) => {
  const response = await api.post(
    `/boards/${b_id}/comments?u_id=${u_id}`,
    commentData,
  );
  return response.data;
};
