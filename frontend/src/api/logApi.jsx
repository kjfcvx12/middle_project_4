import api from "./api";

export const getLogs = async () => {
  const res = await api.get("/logs");
  return res.data;
};

export const createLog = async (data) => {
  const res = await api.post("/logs", data);
  return res.data;
};