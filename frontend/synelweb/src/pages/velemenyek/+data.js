export { data }

import { fetchReviews } from '../../services/reviewsService'

async function data() {
  const reviews = await fetchReviews()
  return {
    reviews
  }
}
