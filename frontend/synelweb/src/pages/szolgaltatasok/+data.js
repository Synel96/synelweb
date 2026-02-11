export { data };

import { fetchPackages } from "../../services/packagesService";

async function data() {
  const response = await fetchPackages();
  const packages = Array.isArray(response.data)
    ? response.data.map(pkg => ({
        ...pkg,
        tags: pkg.tags
          ? pkg.tags.split(",").map(t => t.trim()).filter(Boolean)
          : [],
      }))
    : [];
  return { packages };
}
