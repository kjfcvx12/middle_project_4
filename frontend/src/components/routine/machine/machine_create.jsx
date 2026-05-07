import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { machines_read_detail } from '../../../api/api_machine';
import { machines_create, machines_update } from '../../../api/api_machine';
import { useAuth } from '../../AuthContext';
import { useSearchParams } from "react-router-dom";
import api from '../../../api/api';
import './machine_create.css'

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

    if (authLoading || !userData) {return <div>로딩중...</div>}
    if (loading) return <div>로딩중...</div>

    //생성 권한(관리자)
    if (!isEdit && userData.role !== "admin"){
        return <div className='machine-no-auth'>생성 권한이 없습니다</div>
    }

    //수정 권한
    if (isEdit && userData?.role !== "manager") {
        return <div className='machine-no-auth'>수정 권한 없습니다</div>
    }



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
        
        await api.post("/gym_machines/", {
            g_id: Number(g_id),
            m_id: res.data.m_id,
            qty: 1
        })
        console.log("생성된 m_id:", res.data.m_id)
        console.log(res.data)
        console.log(res.data.m_id)

        alert("생성 완료했습니다")
        nav(`/gyms/${g_id}/machines`)
        }


    } catch (error) {
        console.log(error)
        alert("에러 발생했습니다")
    }
    }


    return (
    <div className='machine-create-container'>

        <div className='machine-create-wrapper'>

        <h1 className='machine-create-title'>
            {isEdit ? "운동기구 수정" : "운동기구 생성"}
        </h1>

        <form
            className='machine-create-form'
            onSubmit={handleSubmit}
        >

            <div className='machine-input-group'>
            <label className='machine-input-label'>
                기구 이름
            </label>

            <input
                className='machine-input'
                name='m_name'
                placeholder='기구 이름 입력'
                value={form.m_name}
                onChange={handleChange}
            />
            </div>

            <div className='machine-input-group'>
            <label className='machine-input-label'>
                운동기구 설명
            </label>

            <textarea
                className='machine-textarea'
                name='dsc'
                placeholder='운동기구 설명 입력'
                value={form.dsc}
                onChange={handleChange}
            />
            </div>

            <div className='machine-input-group'>
            <label className='machine-input-label'>
                이미지 URL
            </label>

            <input
                className='machine-input'
                name='m_url'
                placeholder='이미지 URL 입력'
                value={form.m_url}
                onChange={handleChange}
            />
            </div>

            {form.m_url && (
            <div className='machine-preview-box'>
                <img
                className='machine-preview-image'
                src={form.m_url}
                alt='preview'
                />
            </div>
            )}

            <div className='machine-btn-group'>

            <button
                type="submit"
                className='machine-submit-btn'
            >
                {isEdit ? "수정" : "생성"}
            </button>

            <button
                type='button'
                className='machine-cancel-btn'
                onClick={() => nav(-1)}
            >
                취소
            </button>

            <button
                type="button"
                className='machine-list-btn'
                onClick={() => nav(`/gyms/${g_id}/machines`)}
            >
                기구 목록
            </button>

            </div>

        </form>

        </div>

    </div>
    );
};

export default machine_create;