import { useEffect, useState } from 'react';
import { machines_read_detail } from '../../../api/api_machine';
import { useParams } from 'react-router-dom';


const machine_detail = () => {

  const { m_id } = useParams()

  const [machine, setMachine]=useState(null)
  const[loading, setLoading]=useState(true)


  useEffect(()=>{
    if (!m_id) return

    fetch_machine_detail()
  },[m_id])


  const fetch_machine_detail=async()=>{
    try{
      const response=await machines_read_detail(m_id)

      console.log('상세',response.data)
      setMachine(response.data)
    }catch(error1){
      console.error('상세 조회 실패',error1)
    }finally{
      setLoading(false)
    }
  }

  if(loading) return <div>로딩중...</div>
  return (
    <div>
      <h1>{machine.m_name}</h1>
      <img src={machine.m_url} alt={machine.m_name} width="200" />

      <p>운동기구 설명: {machine.dsc}</p>

    </div>
  );
};

export default machine_detail;