import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { machines_read_detail } from './../../../api/api_machine';
import { useAuth } from "../../AuthContext";
import { machines_read } from '../../../api/api_machine';
import { machines_delete } from '../../../api/api_machine';
import { useSearchParams } from "react-router-dom";
import { gym_machines_get } from '../../../api/gym_machines';
import { gyms_get_machines } from '../../../api/gyms';

const machine_list = () => {

    const { g_id }=useParams()
    const nav=useNavigate()
    const {userData, loading: authLoading}=useAuth()
    console.log("g_id:", g_id);
    console.log("userData:", userData)
    console.log("authLoading:", authLoading)

    const [list, setList]=useState([])
    const [loading, setLoading]=useState(true)

    
    useEffect(()=>{
      if(!g_id){
        setLoading(false)
        return
      }
        fetch_machines()              
    },[g_id])


    const fetch_machines = async () => {
      try {
        const response = await gyms_get_machines(g_id)

        console.log("헬스장 목록", response.data)

        setList(response.data.data || response.data)

      } catch (error1) {
        console.error("목록 조회 실패", error1);
      } finally {
        setLoading(false);
      }
    }


    if (authLoading || loading) return <div>로딩중...</div>


    const handleDelete = async (m_id) => {

      if (!confirm("정말 삭제하시겠습니까?")) {
        alert("삭제가 취소되었습니다.");
        return;
      }

      try {
        await fetch("/gym_machines", {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            g_id: Number(g_id),
            m_id: m_id,
          }),
        });

        alert("삭제가 완료되었습니다.");

        fetch_machines();

      } catch (error) {
        console.error(error);

        alert("삭제 중 오류가 발생했습니다.");
      }
    };


    return (
        <div>
            <h1>운동기구 목록</h1>
            
            {list.map((m)=>(
                <div key={m.m_id} onClick={()=>nav(`/gyms/${g_id}/machines/${m.m_id}`)}>
                    <span>{m.m_name}</span>
                      {/* 삭제 버튼 */}
                    {userData?.role==="admin" && (
                      <button onClick={(e)=>{e.stopPropagation()
                        handleDelete(m.m_id)
                      }}>삭제</button>
                    )}
                </div>
            ))}   
              {/* 생성 버튼 */}
            {userData?.role === "admin" && (
              <button onClick={() => nav(`/gyms/${g_id}/machines/create`)}>
                운동기구 생성
              </button>
            )}

            
        </div>
    );
};

export default machine_list;