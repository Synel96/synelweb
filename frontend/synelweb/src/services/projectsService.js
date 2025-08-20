import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/";

export async function getProjects() {
  const response = await axios.get(`${API_BASE_URL}projects/projects/`);
  return response.data;
}
