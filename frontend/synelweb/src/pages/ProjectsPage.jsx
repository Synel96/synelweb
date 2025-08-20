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
        position: "relative", // háttérhez
        overflow: "hidden",
      }}
      role="main"
      aria-label="Projektek oldal"
      tabIndex={0}
    >
      {/* Animált háttérkép */}
      <img
        src="/projectspage.webp"
        alt=""
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
          zIndex: 1,
          pointerEvents: "none",
          opacity: 0,
          animation: "fadeInBg 1s cubic-bezier(.4,0,.2,1) 0.05s forwards",
        }}
        aria-hidden="true"
      />
      {/* Tartalom */}
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
          opacity: 0,
          animation: "fadeInUp 0.7s cubic-bezier(.4,0,.2,1) 0.1s forwards",
          position: "relative",
          zIndex: 2,
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
          gap: 3, // kisebb gap
          alignItems: { xs: "stretch", sm: "flex-start" },
          justifyContent: { xs: "center", sm: "flex-start" },
          position: "relative",
          zIndex: 2,
        }}
        role="region"
        aria-label="Projektek listája"
        tabIndex={0}
      >
        {loading ? (
          <ProjectsSkeleton />
        ) : (
          projects.map((project, idx) => (
            <Box
              key={project.id}
              sx={{
                opacity: 0,
                animation: `fadeInUp 0.7s cubic-bezier(.4,0,.2,1) ${
                  0.3 + idx * 0.15
                }s forwards`,
                maxWidth: { xs: 320, sm: 280, md: 260 }, // kisebb kártya szélesség
                width: "100%",
              }}
            >
              <ProjectsCard
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
            </Box>
          ))
        )}
      </Box>
      <style>
        {`
          @keyframes fadeInUp {
            from {
              opacity: 0;
              transform: translateY(32px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
          @keyframes fadeInBg {
            from {
              opacity: 0;
            }
            to {
              opacity: 1;
            }
          }
        `}
      </style>
    </Box>
  );
}

export default ProjectsPage;
