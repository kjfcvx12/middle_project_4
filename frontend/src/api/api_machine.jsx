import api from './api';
import machine_create from './../Components/routine/machine/machine_create';

//운동기구 상세 조회
export const machines_read_detail=(m_id)=>{
    return api.get(`/machines/${m_id}`)
}


// 운동기구 생성(admin)
export const machine_create=(data)=>{
    return api.post('/machines',data)
}


