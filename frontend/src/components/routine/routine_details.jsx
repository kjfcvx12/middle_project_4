import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
    routine_detail_create,
    routine_detail_read_all,
    routine_detail_delete,
    routine_detail_update
} from '../../api/routine_details';

import { getParts } from '../../api/parts';
import { machines_read } from './../../api/machines';

import './Routine_details.css';

const Routine_details = () => {

    const { r_id } = useParams();

    const [list, setList] = useState([]);
    const [parts, setParts] = useState([]);
    const [machines, setMachines] = useState([]);

    const [p_id, setP_id] = useState('');

    const [form, setForm] = useState({
        r_d_id: null,
        m_id: '',
        step: '',
        sets: '',
        reps: '',
        rest_time: '',
        weight: '',
    });

    const [editId, setEditId] = useState(null);

    const [editForm, setEditForm] = useState({
        r_d_id: null,
        sets: '',
        reps: '',
        weight: '',
        rest_time: ''
    });

    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {

        if (!r_id) return;

        fetch_routine_details();
        fetch_parts();

    }, [r_id]);

    // 루틴 디테일 리스트
    const fetch_routine_details = async () => {

        try {

            const response = await routine_detail_read_all(r_id);

            setList(response.data.data || []);

        } catch (err) {

            console.error(err.response?.data || err);
        }
    };

    // 부위 리스트 가져오기
    const fetch_parts = async () => {

        try {

            const response = await getParts();

            setParts(response.data.data || response.data);

        } catch (err) {

            console.error(err.response?.data || err);
        }
    };

    // 부위 선택 -> 머신 가져오기
    const handle_part_change = async (e) => {

        const value = Number(e.target.value);

        setP_id(value);

        try {

            const response = await machines_read(value);

            setMachines(response.data.data || response.data);

        } catch (err) {

            console.error(err.response?.data || err);
        }

        setForm((prev) => ({
            ...prev,
            m_id: '',
        }));
    };

    const handle_change = (e) => {

        const { name, value } = e.target;

        setForm((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    // 루틴 디테일 추가
    const handleAdd = async () => {

        if (!form.m_id || !form.sets || !form.reps) {

            alert("운동 / 세트 / 횟수 입력 필요");

            return;
        }

        try {

            await routine_detail_create({

                r_id: Number(r_id),

                m_id: Number(form.m_id),

                step: list.length + 1,

                sets: Number(form.sets),

                reps: Number(form.reps),

                rest_time: Number(form.rest_time || 0),

                weight: Number(form.weight || 0),
            });

            fetch_routine_details();

            setForm({

                r_d_id: null,
                m_id: "",
                step: "",
                sets: "",
                reps: "",
                rest_time: "",
                weight: "",
            });

            setIsOpen(false);

        } catch (err) {

            console.error(err.response?.data || err);
        }
    };

    // 삭제
    const handle_delete = async (r_d_id) => {

        try {

            await routine_detail_delete(r_d_id);

            fetch_routine_details();

        } catch (err) {

            console.error(err);
        }
    };

    // 수정
    const handle_update = async () => {

        try {

            await routine_detail_update(editId, {

                sets: Number(editForm.sets),

                reps: Number(editForm.reps),

                rest_time: Number(editForm.rest_time),

                weight: Number(editForm.weight),
            });

            setEditId(null);

            fetch_routine_details();

        } catch (err) {

            console.error(err);
        }
    }

    // 순서 변경 (위로 올리기)
    const move_up = async (index) => {

        if (index === 0) return;

        const current = list[index];

        const prev = list[index - 1];

        await routine_detail_update(current.r_d_id, {
            step: prev.step
        });

        await routine_detail_update(prev.r_d_id, {
            step: current.step
        });

        fetch_routine_details();
    }

    // 순서 변경 (아래로)
    const move_down = async (index) => {

        if (index === list.length - 1) return;

        const current = list[index];

        const next = list[index + 1];

        await routine_detail_update(current.r_d_id, {
            step: next.step
        });

        await routine_detail_update(next.r_d_id, {
            step: current.step
        });

        fetch_routine_details();
    }

    return (

        <div className='routine-detail-page'>

            <h1>루틴 상세</h1>

            {/* 리스트 */}
            {list.map((ex, i) => (

                <div
                    key={ex.r_d_id}
                    className='detail-card'
                >

                    <h3>{ex.m_name}</h3>

                    {editId === ex.r_d_id &&
                    editForm.r_d_id === ex.r_d_id ? (

                        <div className='edit-box'>

                            <input
                                value={editForm.sets ?? ''}
                                placeholder='세트'
                                onChange={(e) =>
                                    setEditForm({
                                        ...editForm,
                                        sets: e.target.value
                                    })
                                }
                            />

                            <input
                                value={editForm.reps ?? ''}
                                placeholder='횟수'
                                onChange={(e) =>
                                    setEditForm({
                                        ...editForm,
                                        reps: e.target.value
                                    })
                                }
                            />

                            <input
                                value={editForm.weight ?? ''}
                                placeholder='무게'
                                onChange={(e) =>
                                    setEditForm({
                                        ...editForm,
                                        weight: e.target.value
                                    })
                                }
                            />

                            <input
                                value={editForm.rest_time ?? ''}
                                placeholder='휴식 시간'
                                onChange={(e) =>
                                    setEditForm({
                                        ...editForm,
                                        rest_time: e.target.value
                                    })
                                }
                            />

                            <button
                                className='save-btn'
                                onClick={handle_update}
                            >
                                저장
                            </button>

                        </div>

                    ) : (

                        <p className='detail-info'>
                            {ex.sets}세트 x {ex.reps}회 x {ex.weight ?? 0}kg
                        </p>
                    )}

                    <div className='button-wrap'>

                        <button
                            className='edit-btn'
                            onClick={() => {

                                setEditId(ex.r_d_id);

                                setEditForm({

                                    r_d_id: ex.r_d_id,

                                    sets: ex.sets ?? '',

                                    reps: ex.reps ?? '',

                                    weight: ex.weight ?? '',

                                    rest_time: ex.rest_time ?? '',
                                });
                            }}
                        >
                            수정
                        </button>

                        <button
                            className='delete-btn'
                            onClick={() => handle_delete(ex.r_d_id)}
                        >
                            삭제
                        </button>

                        <button
                            className='move-btn'
                            onClick={() => move_up(i)}
                        >
                            ↑
                        </button>

                        <button
                            className='move-btn'
                            onClick={() => move_down(i)}
                        >
                            ↓
                        </button>

                    </div>

                </div>
            ))}

            <button
                className='create-btn'
                onClick={() => setIsOpen(true)}
            >
                + 운동 추가
            </button>

            {isOpen && (

                <div className='modal-box'>

                    <h3>운동 루틴 추가</h3>

                    <select
                        value={p_id}
                        onChange={handle_part_change}
                    >

                        <option value="">부위 선택</option>

                        {Array.isArray(parts) &&
                            parts.map((part) => (

                                <option
                                    key={part.p_id}
                                    value={part.p_id}
                                >
                                    {part.p_name}
                                </option>
                            ))}
                    </select>

                    <select
                        name="m_id"
                        value={form.m_id}
                        onChange={handle_change}
                    >

                        <option value="">운동 선택</option>

                        {machines.map((machine) => (

                            <option
                                key={machine.m_id}
                                value={machine.m_id}
                            >
                                {machine.m_name}
                            </option>
                        ))}
                    </select>

                    <input
                        name="sets"
                        placeholder="세트 수"
                        value={form.sets}
                        onChange={handle_change}
                    />

                    <input
                        name="reps"
                        placeholder="반복 횟수"
                        value={form.reps}
                        onChange={handle_change}
                    />

                    <input
                        name="rest_time"
                        placeholder="휴식 시간"
                        value={form.rest_time}
                        onChange={handle_change}
                    />

                    <input
                        name="weight"
                        placeholder="중량"
                        value={form.weight}
                        onChange={handle_change}
                    />

                    <button
                        className='save-btn'
                        onClick={handleAdd}
                    >
                        추가
                    </button>

                    <button
                        className='delete-btn'
                        onClick={() => setIsOpen(false)}
                    >
                        취소
                    </button>

                </div>
            )}

        </div>
    )
}

export default Routine_details