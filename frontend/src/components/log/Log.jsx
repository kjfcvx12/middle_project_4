import React, { useEffect, useState } from "react";
import "./Log.css";

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
    const m = machines.find((x) => x.m_id === m_id);
    return m?.m_name || `머신 ${m_id}`;
  };

  // 운동량 계산
  const getVolume = (log) =>
    log.details?.reduce(
      (sum, d) => sum + d.sets * d.reps * (d.weight || 0),
      0
    ) || 0;

  // 운동 시간 계산
  const getTime = (log) =>
    (log.details?.reduce(
      (sum, d) => sum + (d.duration || 0),
      0
    ) || 0) / 60;

  return (
    <div className="log-container">
      <h2 className="log-title">운동 기록</h2>

      {logs.length === 0 && (
        <p className="empty-log">아직 기록이 없습니다.</p>
      )}

      {logs.map((log) => (
        <div key={log.log_id} className="log-item">

          <div
            className="log-summary"
            onClick={() =>
              setOpenId(openId === log.log_id ? null : log.log_id)
            }
          >
            <div className="log-date">
              {new Date(log.log_date).toLocaleDateString()}
            </div>

            <div className="log-stats">

              <div className="log-stat-box">
                <div className="log-stat-label">운동량</div>
                <div className="log-stat-value">
                  {getVolume(log)} kg
                </div>
              </div>

              <div className="log-stat-box">
                <div className="log-stat-label">휴식 시간</div>
                <div className="log-stat-value">
                  {Math.round(getTime(log))} 분
                </div>
              </div>

            </div>
          </div>

          {/* 상세 운동 */}
          {openId === log.log_id && (
            <div className="detail-box">

              {log.details?.map((d, i) => (
                <div key={i} className="detail-item">

                  <div className="detail-machine">
                    {getMachineName(d.m_id)}
                  </div>

                  <div className="detail-info">
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
        className="log-btn"
        onClick={() => setIsModalOpen(true)}
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