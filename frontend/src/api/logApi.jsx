import api from "./api";

/**
 * 🔥 로그 목록 조회
 */
export const getLogs = async () => {
  try {
    const res = await api.get("/logs/");
    return res.data;
  } catch (e) {
    console.error("❌ getLogs 실패:", e.response?.data || e);
    throw e;
  }
};

/**
 * 🔥 로그 상세 조회
 */
export const getLogDetail = async (log_id) => {
  try {
    const res = await api.get(`/logs/${log_id}`);
    return res.data;
  } catch (e) {
    console.error("❌ getLogDetail 실패:", e.response?.data || e);
    throw e;
  }
};

/**
 * 🔥 로그 생성
 */
export const createLog = async (data) => {
  try {
    console.log("🔥 createLog payload:", data); // ⭐ 디버깅 핵심

    const res = await api.post("/logs/", data);

    console.log("✅ createLog 성공:", res.data);
    return res.data;
  } catch (e) {
    console.error("❌ createLog 실패:", e.response?.data || e);
    throw e;
  }
};

/**
 * 🔥 로그 삭제
 */
export const deleteLog = async (log_id) => {
  try {
    const res = await api.delete(`/logs/${log_id}`);
    return res.data;
  } catch (e) {
    console.error("❌ deleteLog 실패:", e.response?.data || e);
    throw e;
  }
};