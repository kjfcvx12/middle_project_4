import api from "./api";

// 운동 추가
export const routine_detail_create = ({r_id, m_id, step, sets, reps, rest_time})=>{
    return api.post("/routine_details", {
        r_id, m_id, setp, sets, reps, rest_time
    });
};

// 루틴 운동 리스트
export const routine_detail_read_all = (r_id) =>{
    return api.get(`/routine_details/${r_id}`);
};

// 단일 운동 조회
export const routine_detail_read_one = (r_d_id) => {
    return api.get(`/routine_details/one/${r_d_id}`)
}

// 운동 수정
export const routine_detail_update = (r_d_id, {step, sets, reps, rest_time}) =>{
    return api.put(`/routine_details/${r_d_id}`,{
        step, sets, reps, rest_time,
    });
};

// 운동 삭제
export const routine_detail_delete = (r_d_id) =>{
    return api.delete(`/routine_details/${r_d_id}`);
};