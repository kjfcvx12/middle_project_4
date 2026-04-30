import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';




const machine_create = () => {

    const nav=useNavigate()
    const { user }=useAuth()

    const [form, setForm]=useState({
        m_name:'',
        dsc:'',
        m_url:'',
        p_id:''
    })

    const handleChange=(e)=>{
        const { name,value}=e.target
        setForm({...form,[name]:value})
    }

    const handleSubmit=()=>{
        
    }

    return (
        <div>
            <h1>운동기구 추가</h1>
            
        </div>
    );
};

export default machine_create;