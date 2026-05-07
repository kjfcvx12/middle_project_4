import React, { useEffect, useState } from "react";
import { getLogs } from "../../api/logApi";
import LogModal from "./LogModal";
import { machines_read } from "../../api/machines";



const Log = () => {
    const [logs, setLogs] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [machines, setMachines] = useState([]);
    const [openId, setOpenId] = useState(null);

    const fetchLogs = async () => {
        const data = await getLogs();
        setLogs(data);
    };

    const fetchMachines = async () => {
        const res = await machines_read();
        setMachines(res.data.data);
    };

    



    useEffect(() => {
        fetchLogs();
        fetchMachines();
    }, []);


    const getMachineName = (m_id) => {
        const m = machines.find(x => x.m_id === m_id);
        return m?.m_name || `머신 ${m_id}`;
    };

    // 볼륨
    const getVolume = (log) =>
        log.details?.reduce(
            (sum, d) => sum + d.sets * d.reps * (d.weight || 0),
            0
        ) || 0;
        

    // 시간
    const getTime = (log) =>
        (log.details?.reduce(
            (sum, d) => sum + (d.duration || 0),
            0
        ) || 0) / 60;

    return (
        <div style={{ padding: 20, backgroundColor: '#1a1a1a', minHeight: '100vh' }}>
            <h1 style={{ textAlign: 'center', color: 'white', marginBottom: 20 }}>
                운동기록
            </h1>

            {logs.length === 0 && <p>아직 기록이 없습니다</p>}

            {/* 리스트 */}
            {logs.map(log => (
                <div key={log.log_id} style={item}>
                    
                    {/* ⭐ [수정] 클릭하면 상세 열림 */}
                    <div
                        onClick={() =>
                            setOpenId(openId === log.log_id ? null : log.log_id)
                        }
                        style={{ cursor: "pointer" }}
                    >
                        <div>
                            {new Date(log.log_date).toLocaleDateString()} {/* ⭐ 날짜만 표시 */}
                        </div>
                        <div>볼륨: {getVolume(log)} kg</div>
                        <div>시간: {Math.round(getTime(log))} 분</div>
                    </div>

                    {/* ⭐ [추가] 상세 운동 목록 */}
                    {openId === log.log_id && (
                        <div style={detailBox}>
                            {log.details?.map((d, i) => (
                                <div key={i} style={detailItem}>
                                    
                                    {/* ⭐ 머신 이름 표시 */}
                                    <div style={{ fontWeight: "bold" }}>
                                        {getMachineName(d.m_id)}
                                    </div>

                                    <div>
                                        {d.sets}세트 × {d.reps}회
                                    </div>

                                </div>
                            ))}
                        </div>
                    )}
                </div>
            ))}



            {/* 버튼 */}
            <button
                onClick={() => setIsModalOpen(true)}
                style={btn}
            >
                운동 기록하기
            </button>


            {/* 모달 */}
            <LogModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onSuccess={fetchLogs}
            />
        </div>
    );
};

export default Log;

const item = {
    backgroundColor: '#262626', // 피그마 카드 배경색
    borderRadius: '12px',
    padding: '16px',
    marginBottom: '12px',
    color: '#fff',
    boxShadow: '0 4px 6px rgba(0,0,0,0.2)',
};

// 상단 정보 영역 (날짜, 볼륨, 시간)
const summaryContainer = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    cursor: "pointer",
};

const dateText = {
    fontSize: '14px',
    color: '#aaa',
    marginBottom: '4px',
};

const statsText = {
    fontSize: '16px',
    fontWeight: 'bold',
    color: '#ff5722', // 피그마 오렌지 포인트
};

// 상세 정보 박스 (아코디언 열렸을 때)
const detailBox = {
    marginTop: '15px',
    paddingTop: '15px',
    borderTop: '1px solid #3d3d3d',
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
};

const detailItem = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#333',
    padding: '10px 14px',
    borderRadius: '8px',
};

// 하단 '운동 기록하기' 버튼
const btn = {
    width: "100%",
    marginTop: 20,
    padding: '16px',
    backgroundColor: "#ff5722", // 강조 오렌지색
    color: "white",
    border: "none",
    borderRadius: "12px",
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: "pointer",
    boxShadow: '0 4px 12px rgba(255, 87, 34, 0.3)',
};