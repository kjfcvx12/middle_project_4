import api from './api';

//운동기구 상세 조회
export const machines_read_detail=(m_id)=>{
    return api.get(`/machines/${m_id}`)
}