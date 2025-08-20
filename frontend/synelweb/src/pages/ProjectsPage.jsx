import { useEffect, useState } from "react";
import { Box, Typography } from "@mui/joy";
import ProjectsCard from "../components/projects/ProjectsCard";
import ProjectsSkeleton from "../components/projects/ProjectsSkeleton";
import { getProjects } from "../services/projectsService";

function ProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getProjects()
      .then((data) => {
        setProjects(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <Box
      component="main"
      sx={{
        width: "100%",
        minHeight: "80vh",
        display: "flex",
        flexDirection: "column",
        alignItems: { xs: "flex-start", sm: "flex-start", md: "flex-start" },
        justifyContent: "flex-start",
        px: { xs: 2, sm: 4, md: 8 },
        py: { xs: 3, sm: 4 },
      }}
      role="main"
      aria-label="Projektek oldal"
      tabIndex={0}
    >
      <Typography
        level="h1"
        tabIndex={0}
        sx={{
          fontSize: { xs: "2rem", sm: "2.5rem", md: "3rem" },
          fontWeight: 700,
          color: "text.primary",
          letterSpacing: "0.02em",
          mb: 2,
          textAlign: "left",
        }}
        aria-label="Projektek"
      >
        Projektek
      </Typography>
      <Box
        sx={{
          width: "100%",
          display: "flex",
          flexDirection: { xs: "column", sm: "row" },
          flexWrap: "wrap",
          gap: 4,
          alignItems: { xs: "stretch", sm: "flex-start" },
          justifyContent: { xs: "center", sm: "flex-start" },
        }}
        role="region"
        aria-label="Projektek listája"
        tabIndex={0}
      >
        {loading ? (
          <ProjectsSkeleton />
        ) : (
          projects.map((project, idx) => (
            <ProjectsCard
              key={project.id}
              title={project.name}
              description={project.description}
              tags={project.slug ? [project.slug] : []}
              projectVideo={project.preview_video || ""}
              previewImage={project.preview_image || ""}
              images={
                project.extra_images
                  ? project.extra_images.map((img) =>
                      img.image.startsWith("http")
                        ? img.image
                        : `http://localhost:8000${img.image_url}`
                    )
                  : []
              }
              link={project.link || ""}
            />
          ))
        )}
      </Box>
    </Box>
  );
}

export default ProjectsPage;
