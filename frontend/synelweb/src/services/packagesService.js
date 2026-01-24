import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export function fetchPackages() {
  return axios.get(`${BASE_URL}/packages/list/`);
}
