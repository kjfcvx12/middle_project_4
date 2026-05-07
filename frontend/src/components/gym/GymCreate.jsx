import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { gyms_create } from "../../api/gyms.jsx";
import "./GymForm.css";

export default function GymCreate() {
    const nav = useNavigate();

    const [form, setForm] = useState({
        g_name: "",
        g_addr: "",
        g_tel: "",
        open_time: "",
        shower: false,
        parking: false,
        elev: false
    });

    const onChange = (e) => {
        const { name, value, type, checked } = e.target;
        setForm((p) => ({
            ...p,
            [name]: type === "checkbox" ? checked : value
        }));
    };

    const submit = async () => {
        try {
            await gyms_create(form);
            alert("생성 완료");
            nav("/gym");
        } catch (e) {
            alert("생성 실패");
        }
    };

    return (
        <div className="gym-form-page">
            <div className="gym-form-card">

                <h2>헬스장 생성</h2>

                <input name="g_name" placeholder="이름" onChange={onChange} />
                <input name="g_addr" placeholder="주소" onChange={onChange} />
                <input name="g_tel" placeholder="전화번호" onChange={onChange} />
                <input name="open_time" placeholder="운영시간" onChange={onChange} />

                <label><input type="checkbox" name="shower" onChange={onChange} /> 샤워실</label>
                <label><input type="checkbox" name="parking" onChange={onChange} /> 주차장</label>
                <label><input type="checkbox" name="elev" onChange={onChange} /> 엘리베이터</label>

                <button onClick={submit}>생성</button>
            </div>
        </div>
    );
}