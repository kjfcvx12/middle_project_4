import api from './api';

// 특정 헬스장 운동기구 조회
export const gym_machines_get = async (g_id) => {
    return await api.get(`/gyms/${g_id}/machines`);
};