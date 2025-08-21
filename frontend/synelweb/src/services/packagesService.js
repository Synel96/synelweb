import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export function fetchPackages() {
  return axios.get(`${BASE_URL}/packages/list/`);
}
