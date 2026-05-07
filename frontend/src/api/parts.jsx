import api from "./api";

export const getParts = () => {
  return api.get("/parts");
};

export const createParts=(data)=>{
  return api.post("/parts/create", data)
};

export const deleteParts = (p_id) => {
  return api.delete(`/parts/del/${p_id}`);
};