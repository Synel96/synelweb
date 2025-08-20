import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function fetchReviews() {
  const response = await axios.get(`${API_BASE_URL}/review/reviews/`);
  return response.data;
}

export async function postReview(reviewData) {
  const response = await axios.post(
    `${API_BASE_URL}/review/reviews/`,
    reviewData,
    {
      headers: { "Content-Type": "application/json" },
    }
  );
  return response.data;
}
