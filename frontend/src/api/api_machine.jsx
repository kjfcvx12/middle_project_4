import api from './api';


//운동기구 목록(p_id랑 keyword 으로 특정 기구 조회)
export const machine_read=({keyword, p_id}={})=>{
    return api.get('/machines',{
        params:{keyword,p_id}
    })
}


//운동기구 상세 조회
export const machines_read_detail=(m_id)=>{
    return api.get(`/machines/${m_id}`)
}