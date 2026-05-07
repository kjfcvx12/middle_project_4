import { useEffect, useState } from 'react';
import { machines_read_detail } from '../../../api/api_machine';
import { useParams } from 'react-router-dom';
import { useAuth } from '../../AuthContext';
import { useNavigate } from 'react-router-dom';
import './machine_detail.css'

const machine_detail = () => {

  const { g_id, m_id } = useParams()
  const { userData } = useAuth()

  const nav = useNavigate();

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

if (loading) {
  return (
    <div className='machine-detail-loading'>
      로딩중...
    </div>
  );
}

  return (
    <div className='machine-detail-container'>

      <div className='machine-detail-wrapper'>

        <h1 className='machine-detail-title'>
          {machine.m_name}
        </h1>

        <div className='machine-detail-image-box'>
          <img
            className='machine-detail-image'
            src={machine.m_url}
            alt={machine.m_name}
          />
        </div>

        <div className='machine-detail-content'>
          <div className='machine-detail-label'>
            운동기구 설명
          </div>

          <p className='machine-detail-description'>
            {machine.dsc}
          </p>
        </div>

        <div className='machine-detail-btn-group'>

          <button
            className='machine-back-btn'
            onClick={() => nav(`/gyms/${g_id}/machines`)}
          >
            기구 목록으로
          </button>

          {userData?.role === "manager" && (
            <button
              className='machine-edit-btn'
              onClick={() =>
                nav(`/gyms/${g_id}/machines/edit/${machine.m_id}`)
              }
            >
              수정
            </button>
          )}

        </div>

      </div>

    </div>
  );
};

export default machine_detail;