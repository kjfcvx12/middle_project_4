import React, { useEffect, useState } from "react";
import { getLogs } from "../../api/logApi";
import LogModal from "./LogModal";

const Log = () => {
    const [logs, setLogs] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const fetchLogs = async () => {
        const data = await getLogs();
        setLogs(data);
    };

    useEffect(() => {
        fetchLogs();
    }, []);

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
        <div style={{ padding: 20 }}>
            <h2>운동기록</h2>

            {/* 리스트 */}
            {logs.map(log => (
                <div key={log.log_id} style={item}>
                    <div>
                        {new Date(log.log_date).toLocaleString()}
                    </div>
                    <div>볼륨: {getVolume(log)} kg</div>
                    <div>시간: {Math.round(getTime(log))} 분</div>
                </div>
            ))}

            {/* 버튼 */}
            <button onClick={() => setIsModalOpen(true)} style={btn}>
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
    padding: 10,
    borderBottom: "1px solid #ddd",
};

const btn = {
    width: "100%",
    marginTop: 20,
    padding: 15,
    backgroundColor: "black",
    color: "white",
};