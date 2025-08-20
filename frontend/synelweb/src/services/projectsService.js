const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/";

export async function getProjects() {
  const response = await fetch(`${API_BASE_URL}projects/projects/`);
  if (!response.ok) {
    throw new Error("Nem sikerült lekérni a projekteket");
  }
  return await response.json();
}
