// GymEdit.jsx

import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { X } from "lucide-react";
import { gyms_detail, gyms_update } from "../../api/gyms.jsx";
import "./GymForm.css";

export default function GymEdit() {
    const { id } = useParams();
    const nav = useNavigate();

    const [form, setForm] = useState(null);

    useEffect(() => {
        (async () => {
            try {
                const res = await gyms_detail(id);

                setForm({
                    g_name: res.data.g_name || "",
                    g_addr: res.data.g_addr || "",
                    g_tel: res.data.g_tel || "",
                    open_time: res.data.open_time || "",
                    shower: !!res.data.shower,
                    parking: !!res.data.parking,
                    elev: !!res.data.elev
                });
            } catch {
                alert("데이터 불러오기 실패");
                nav("/gym");
            }
        })();
    }, [id, nav]);

    const onChange = (e) => {
        const { name, value, type, checked } = e.target;

        setForm((prev) => ({
            ...prev,
            [name]: type === "checkbox" ? checked : value
        }));
    };

    const validate = () => {
        if (
            form.g_name.trim() === "" ||
            form.g_addr.trim() === "" ||
            form.g_tel.trim() === "" ||
            form.open_time.trim() === ""
        ) {
            alert("모든 항목을 입력해주세요.");
            return false;
        }

        return true;
    };

    const submit = async () => {
        if (!validate()) return;

        try {
            await gyms_update(id, {
                ...form,
                g_name: form.g_name.trim(),
                g_addr: form.g_addr.trim(),
                g_tel: form.g_tel.trim(),
                open_time: form.open_time.trim()
            });

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

                <button
                    type="button"
                    className="gym-close-btn"
                    onClick={() => nav("/gym")}
                >
                    <X size={18} />
                </button>

                <h2>헬스장 수정</h2>

                <input
                    name="g_name"
                    placeholder="이름 *"
                    value={form.g_name}
                    onChange={onChange}
                />

                <input
                    name="g_addr"
                    placeholder="주소 *"
                    value={form.g_addr}
                    onChange={onChange}
                />

                <input
                    name="g_tel"
                    placeholder="전화번호 *"
                    value={form.g_tel}
                    onChange={onChange}
                />

                <input
                    name="open_time"
                    placeholder="운영시간 *"
                    value={form.open_time}
                    onChange={onChange}
                />

                <label>
                    <input
                        type="checkbox"
                        name="shower"
                        checked={form.shower}
                        onChange={onChange}
                    />
                    샤워실
                </label>

                <label>
                    <input
                        type="checkbox"
                        name="parking"
                        checked={form.parking}
                        onChange={onChange}
                    />
                    주차장
                </label>

                <label>
                    <input
                        type="checkbox"
                        name="elev"
                        checked={form.elev}
                        onChange={onChange}
                    />
                    엘리베이터
                </label>

                <button type="button" onClick={submit}>
                    수정
                </button>

            </div>
        </div>
    );
}