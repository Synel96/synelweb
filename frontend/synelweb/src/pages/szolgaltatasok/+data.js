export { data }

import { fetchPackages } from '../../services/packagesService'

async function data() {
  const packages = await fetchPackages()
  return {
    packages
  }
}
