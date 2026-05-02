import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { machines_read_detail } from './../../../api/api_machine';
import { useAuth } from "../../AuthContext";
import { machines_read } from '../../../api/api_machine';
import { machines_delete } from '../../../api/api_machine';

const machine_list = () => {

    const nav=useNavigate()

    const [list, setList]=useState([])
    const [loading, setLoading]=useState(true)
    const { userData, loading: authLoading } = useAuth();

    
    useEffect(()=>{
        fetch_machines()              
    },[])




    const fetch_machines = async () => {
      try {
        const response = await machines_read()

        console.log("목록 전체 응답", response.data)

        setList(response.data.data || response.data)

      } catch (error1) {
        console.error("목록 조회 실패", error1);
      } finally {
        setLoading(false);
      }
    }


    if (authLoading || loading) return <div>로딩중...</div>


    const handleDelete=async(m_id)=>{
      if(!confirm("삭제하시겠습니다")) return

      try{
        await machines_delete(m_id)
        alert("삭제 완료했습니다")
        fetch_machines()
      }catch(error2){
        console.error(error2)
        alert("삭제 실패했습니다")
      }
    }

    return (
        <div>
            <h1>운동기구 목록</h1>

            {list.map((m)=>(
                <div key={m.m_id} onClick={()=>nav(`/machines/${m.m_id}`)}>
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
              <button onClick={() => nav("/machines/create")}>
                운동기구 생성
              </button>
            )}




            
        </div>
    );
};

export default machine_list;