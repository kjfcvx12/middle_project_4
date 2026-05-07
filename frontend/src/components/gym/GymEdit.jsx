import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { gyms_detail, gyms_update } from "../../api/gyms.jsx";
import "./GymForm.css";

export default function GymEdit() {
    const { id } = useParams();
    const nav = useNavigate();

    const [form, setForm] = useState(null);

    useEffect(() => {
        (async () => {
            const res = await gyms_detail(id);
            setForm(res.data);
        })();
    }, [id]);

    const onChange = (e) => {
        const { name, value, type, checked } = e.target;
        setForm((p) => ({
            ...p,
            [name]: type === "checkbox" ? checked : value
        }));
    };

    const submit = async () => {
        try {
            await gyms_update(id, form);
            alert("수정 완료");
            nav("/gym");
        } catch {
            alert("수정 실패");
        }
    };

    if (!form) return <div>loading...</div>;

    return (
        <div className="gym-form-page">
            <div className="gym-form-card">

                <h2>헬스장 수정</h2>

                <input name="g_name" value={form.g_name} onChange={onChange} />
                <input name="g_addr" value={form.g_addr} onChange={onChange} />
                <input name="g_tel" value={form.g_tel} onChange={onChange} />
                <input name="open_time" value={form.open_time} onChange={onChange} />

                <label>
                    <input
                        type="checkbox"
                        name="shower"
                        checked={form.shower}
                        onChange={onChange}
                    /> 샤워실
                </label>

                <label>
                    <input
                        type="checkbox"
                        name="parking"
                        checked={form.parking}
                        onChange={onChange}
                    /> 주차장
                </label>

                <label>
                    <input
                        type="checkbox"
                        name="elev"
                        checked={form.elev}
                        onChange={onChange}
                    /> 엘리베이터
                </label>

                <button onClick={submit}>수정</button>
            </div>
        </div>
    );
}