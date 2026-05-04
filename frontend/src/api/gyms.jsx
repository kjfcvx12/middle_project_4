import api from './api';

// CREATE (관리자)
export const gyms_create = async (data) => {
    return await api.post('/gyms', data);
};

// LIST (페이지, 정렬, 필터)
export const gyms_list = async ({ page = 1, size = 10, sort, name, address } = {}) => {
    return await api.get('/gyms', {
        params: { page, size, sort, name, address }
    });
};

// SEARCH
export const gyms_search = async ({ name, address }) => {
    return await api.get('/gyms/search', {
        params: { name, address }
    });
};

// DETAIL
export const gyms_detail = async (g_id) => {
    return await api.get(`/gyms/${g_id}`);
};

// UPDATE (매니저/관리자)
export const gyms_update = async (g_id, data) => {
    return await api.put(`/gyms/${g_id}`, data);
};

// DELETE (관리자)
export const gyms_delete = async (g_id) => {
    return await api.delete(`/gyms/${g_id}`);
};

// STAFF 조회
export const gyms_get_staffs = async (g_id) => {
    return await api.get(`/gyms/${g_id}/staff`);
};

// MACHINES 조회
export const gyms_get_machines = async (g_id) => {
    return await api.get(`/gyms/${g_id}/machines`);
};