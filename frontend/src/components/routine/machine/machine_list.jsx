import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { machines_read_detail } from './../../../api/api_machine';

const machine_list = () => {

    const nav=useNavigate()

    const [list, setList]=useState([])
    const [loading, setLoading]=useState(true)

    useEffect(()=>{
        fetch_machines()              
    },[])

  const fetch_machines=async ()=>{
    try{
      const response=await machines_read()

      console.log('목록', response.data.data)

      setList(response.data.data);
    } catch (error){
      console.error('목록 조회 실패', error)
    } finally{
      setLoading(false)
    }
  }

  if (loading) return <div>로딩중...</div>


    return (
        <div>
            <h1>운동기구 목록</h1>

            {list.map((m)=>(
                <div key={m.m_id} onClick={()=>nav(`/machines/${m.m_id}`)}>
                    {m.m_name}
                </div>
            ))}   
        </div>
    );
};

export default machine_list;