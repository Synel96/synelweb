export { data }

import { getProjects } from '../../services/projectsService'

async function data() {
  const projects = await getProjects()
  return {
    projects
  }
}
