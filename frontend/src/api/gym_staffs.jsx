import api from './api';

// 특정 헬스장 직원 조회
export const gym_staffs_get = async (g_id) => {
    return await api.get(`/gyms/${g_id}/staff`);
};