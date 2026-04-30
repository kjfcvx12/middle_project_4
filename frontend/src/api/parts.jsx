import api from "./api";

export const getParts = () => {
  return api.get("/parts");
};