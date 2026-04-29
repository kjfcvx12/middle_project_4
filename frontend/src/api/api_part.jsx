import api from './api';

// 운동 부위 목록 조회
export const parts_read=()=>{
  return api.get('/parts');
};