import api from './api';

// 루틴 생성
export const routines_create = ({r_name, u_id, p_id})=>{
    return api.post('/routines',{ r_name,u_id,p_id,});
};

// 루틴 목록 조회 (쿼리 포함)
export const routines_read = ({name, p_id, u_id}={}) =>{
    return api.get("/routines",{
        params : {name, p_id,u_id}
    },);
};

// 루틴 상세 (디테일 아님)
export const routines_read_detail = (r_id) =>{
    return api.get(`/routines/${r_id}`);
};

// 루틴 수정
export const routines_update = (r_id, {r_name,p_id}) =>{
    return api.put(`/routines/${r_id}`,{r_name, p_id,});
};

// 루틴 삭제
export const routines_delete = (r_id) =>{
    return api.delete(`/routines/${r_id}`);
};