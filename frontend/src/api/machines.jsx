import api from "./api";

export const machines_read = (p_id) => {
  return api.get("/machines", {
    params: { p_id },
  });
};