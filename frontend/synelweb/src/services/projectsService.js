import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/";

// Simple in-memory cache with TTL
const cache = {
  data: null,
  timestamp: 0,
  ttl: 5 * 60 * 1000, // 5 minutes
};

export async function getProjects() {
  // Check if cache is valid
  const now = Date.now();
  if (cache.data && (now - cache.timestamp) < cache.ttl) {
    return cache.data;
  }

  // Fetch fresh data
  const response = await axios.get(`${API_BASE_URL}projects/projects/`, {
    // Add timeout to prevent hanging
    timeout: 10000,
  });
  
  // Update cache
  cache.data = response.data;
  cache.timestamp = now;
  
  return response.data;
}
