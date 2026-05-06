import React, { useEffect, useState } from "react";
import { createLog } from "../../api/logApi";
import { machines_read } from "../../api/machines";
import { routines_read } from "../../api/routines";
import { routine_detail_read_all } from "../../api/routine_details";

const LogModal = ({ isOpen, onClose, onSuccess }) => {
    const [mode, setMode] = useState("");

    const [routines, setRoutines] = useState([]);
    const [machines, setMachines] = useState([]);

    const [r_id, setRId] = useState("");
    const [m_id, setMId] = useState("");

    const [details, setDetails] = useState([]);

    // 데이터 로딩
    useEffect(() => {
        if (!isOpen) return;

        routines_read().then(res => {
        console.log("routines:", res.data.data);
        setRoutines(res.data.data); 
    });

        machines_read().then(res => {
            console.log("machines 응답:", res);
            setMachines(res.data.data); 
        });
    }, [isOpen]);

    if (!isOpen) return null;

    // =========================
    // 루틴 선택 → 자동 채움
    // =========================
    const handleRoutineChange = async (value) => {
    const selected = routines.find(r => r.r_id === Number(value));
    setRId(Number(value));

    if (!selected) return;

    try {
        
        const res = await routine_detail_read_all(selected.r_id);
        console.log("detail 응답:", res);

        const detailList = res.data.data; 

        const newDetails = detailList.map(d => ({
            m_id: d.m_id,
            sets: d.sets,
            reps: d.reps,
            weight: 0,
            duration: 60,
            fail_memo: "",
            memo: "기록",
        }));

        setDetails(newDetails);

    } catch (e) {
        console.log("detail 불러오기 실패", e);
    }
};

    // =========================
    // detail 수정
    // =========================
    const updateDetail = (i, field, value) => {
        const copy = [...details];
        copy[i][field] = value;
        setDetails(copy);
    };

    // =========================
    // detail 추가
    // =========================
    const addDetail = () => {
        setDetails([
            ...details,
            {
                m_id: machines[0]?.m_id || 1,
                sets: 3,
                reps: 10,
                weight: 0,
                duration: 60,
                fail_memo: "",
                memo: "기록"
            },
        ]);
    };

    // =========================
    // 저장
    // =========================
    const handleSave = async () => {
        try {
            const payload = {
                r_id: mode === "routine" ? r_id : 1,
                attend: true,
                details: details.map(d => ({
                    m_id: d.m_id,
                    
                    sets: Number(d.sets),
                    reps: Number(d.reps),
                    weight: Number(d.weight) || 0,
                    duration: Number(d.duration) || 0,
                    fail_memo: d.fail_memo || "",
                    memo: d.memo || "기록"
                })),
            
                
            };
            console.log("🔥 payload:", payload);
            await createLog(payload);

            onSuccess();
            onClose();
        } catch (e) {
            console.log("저장 실패", e);
        }
    };

    return (
        <div style={overlay}>
            <div style={modal}>
                <h3>운동 기록</h3>

                {/* 모드 선택 */}
                {!mode && (
                    <div style={modeBox}>
                        <button onClick={() => setMode("routine")}>
                            루틴 선택하기
                        </button>
                        <button onClick={() => {
                            setMode("manual");
                            setDetails([
                                {
                                    m_id: 1,
                                    sets: 3,
                                    reps: 10,
                                    weight: 0,
                                    duration: 60,
                                    fail_memo: "",
                                    memo:  "기록" ,
                                }
                            ]);
                        }}>
                            직접 입력하기
                        </button>
                    </div>
                )}

                {/* 루틴 모드 */}
                {mode === "routine" && (
                    <>
                        <select onChange={(e) => handleRoutineChange(e.target.value)}>
                            <option>루틴 선택</option>
                            {routines.map(r => (
                            <option key={r.r_id} value={r.r_id}>
                                {r.r_name}
                            </option>
                        ))}
                        </select>
                    </>
                )}

                {/* detail 입력 */}
                {mode && details.map((d, i) => (
                    <div key={i} style={box}>
                        <select
                            value={d.m_id}
                            onChange={(e) =>
                                updateDetail(i, "m_id", Number(e.target.value))
                            }
                        >
                            {machines.map(m => (
                                <option key={m.m_id} value={m.m_id}>
                                    {m.m_name}
                                </option>
                            ))}
                        </select>

                        <input type="number" value={d.sets}
                            onChange={(e) => updateDetail(i, "sets", Number(e.target.value))}
                        />
                        <input type="number" value={d.reps}
                            onChange={(e) => updateDetail(i, "reps", Number(e.target.value))}
                        />

                        <input type="number" placeholder="무게"
                            value={d.weight}
                            onChange={(e) => updateDetail(i, "weight", Number(e.target.value))}
                        />

                        <input type="number" placeholder="시간(초)"
                            value={d.duration}
                            onChange={(e) => updateDetail(i, "duration", Number(e.target.value))}
                        />

                        <input placeholder="실패 메모"
                            value={d.fail_memo}
                            onChange={(e) => updateDetail(i, "fail_memo", e.target.value)}
                        />

                        <input placeholder="메모"
                            value={d.memo}
                            onChange={(e) => updateDetail(i, "memo", e.target.value)}
                        />
                    </div>
                ))}

                {mode && (
                    <>
                        <button onClick={addDetail}>+ 추가</button>

                        <div style={{ marginTop: 10 }}>
                            <button onClick={() => setMode("")}>뒤로</button>
                            <button onClick={onClose}>취소</button>
                            <button onClick={handleSave}>저장</button>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default LogModal;

// 스타일
const overlay = {
    position: "fixed", top: 0, left: 0, right: 0, bottom: 0,
    background: "rgba(0,0,0,0.5)",
    display: "flex", justifyContent: "center", alignItems: "center",
};

const modal = {
    background: "white",
    padding: "20px",
    width: "90%",
    maxWidth: "420px",
    borderRadius: "10px",
};

const box = {
    marginTop: "10px",
    display: "flex",
    flexDirection: "column",
    gap: "5px",
};

const modeBox = {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
};