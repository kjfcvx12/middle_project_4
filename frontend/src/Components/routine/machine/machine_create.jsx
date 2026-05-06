import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { machines_read_detail } from '../../../api/api_machine';
import { machines_create, machines_update } from '../../../api/api_machine';
import { useAuth } from '../../AuthContext';
import { useSearchParams } from "react-router-dom";
import api from '../../../api/api';


const machine_create = () => {

    const {g_id, m_id}=useParams()

    const nav=useNavigate()
    const { userData, loading: authLoading }=useAuth()

    const isEdit=!!m_id

    const [form, setForm]=useState({
        m_name:'',
        dsc:'',
        m_url:'',
    })
    console.log("보내는 form:", form)
    console.log("g_id:", g_id)
    console.log("userData:", userData)
    console.log("authLoading:", authLoading)
    console.log("isEdit:", isEdit)


    const [loading, setLoading]=useState(false)

    if (authLoading || !userData) {return <div>로딩중...</div>}
    if (loading) return <div>로딩중...</div>

    //생성 권한(관리자)
    if (!isEdit && userData.role !== "admin"){
        return <div>생성 권한이 없습니다</div>
    }

    //수정 권한
    if (isEdit && userData?.role !== "manager") {
        return <div>수정 권한 없음</div>
    }

    useEffect(()=>{
        if(!isEdit){
            setLoading(false)
            return
        }

        setLoading(true)

        const fetch_machine = async () => {
            try{
                const res = await machines_read_detail(m_id)
                setForm(res.data.data || res.data)
            }catch(e){
                console.error(e)
            }finally{
                setLoading(false)
            }
        }

        fetch_machine()
    },[m_id])


  const handleChange=(e)=>{
    const { name, value }=e.target
    setForm({ ...form, [name]:value})
  }

    const handleSubmit = async (e) => {
    e.preventDefault()


    try {
        if (isEdit) {
        await machines_update(m_id, form)
        alert("수정 완료했습니다")
        nav(`/gyms/${g_id}/machines/${m_id}`)
        } else {
        const res = await machines_create(form)
        
        await api.post("/gym_machines", {
            g_id: Number(g_id),
            m_id: res.data.m_id,
            qty: 1
        })
        console.log("생성된 m_id:", res.data.m_id)

        alert("생성 완료했습니다")
        nav(`/gyms/${g_id}/machines`)
        }


    } catch (error) {
        console.log(error)
        alert("에러 발생했습니다")
    }
    }


    return (
        <div>
            <h1>{isEdit? "운동기구 수정":"운동기구 생성"}</h1>

            <form onSubmit={handleSubmit}>

                <input
                name='m_name'
                placeholder='기구 이름'
                value={form.m_name}
                onChange={handleChange}/>

                <input
                name='dsc'
                placeholder='설명'
                value={form.dsc}
                onChange={handleChange}/>


                <input
                name="m_url"
                placeholder='이미지 URL'
                value={form.m_url}
                onChange={handleChange}/>

                <button type="submit">{isEdit ? "수정":"생성"}</button>
                <button type='button' onClick={()=>nav(-1)}>취소</button>


            </form>

        </div>
    );
};

export default machine_create;