import { useEffect, useState } from "react";
import { Box, Typography, Sheet } from "@mui/joy";
import ProjectsCard from "../components/projects/ProjectsCard";
import ProjectsSkeleton from "../components/projects/ProjectsSkeleton";
import { getProjects } from "../services/projectsService";
import { useColorScheme } from "@mui/joy/styles";
import OptimizedBackgroundImage from "../components/common/OptimizedBackgroundImage";

function ProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const { mode } = useColorScheme();

  useEffect(() => {
    getProjects()
      .then((data) => {
        setProjects(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <Sheet
      component="section"
      sx={{
        position: "relative",
        width: "100vw",
        minHeight: { xs: "60vw", sm: "60vw", md: "60vw" },
        maxHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        overflow: "hidden",
        p: 0,
        m: 0,
        transition: "background 0.3s",
      }}
      variant="plain"
      role="region"
      aria-label="Projektek oldal szekció"
      tabIndex={0}
    >
      {/* Cloudinary optimalizált háttérkép */}
      <OptimizedBackgroundImage 
        cloudinaryId="projectspage_fxqkwn"
        alt="Projektek oldal háttérkép"
      />
      {/* Tartalom */}
      <Box
        sx={{
          position: "relative",
          zIndex: 2,
          mt: { xs: 4, sm: 6 },
          mb: 2,
          p: { xs: 2, sm: 4 },
          borderRadius: 4,
          backgroundColor:
            mode === "dark" ? "rgba(30,30,30,0.85)" : "rgba(255,255,255,0.85)",
          boxShadow: "md",
          width: { xs: "95%", sm: "80%", md: "720px" },
          mx: "auto",
          textAlign: { xs: "center", sm: "left" }, // mobilon középen, asztalon balra
          opacity: 0,
          animation: "fadeInUp 0.7s cubic-bezier(.4,0,.2,1) 0.1s forwards",
        }}
      >
        <Typography
          level="h1"
          tabIndex={0}
          sx={{
            fontSize: { xs: "2rem", sm: "2.5rem", md: "3rem" },
            fontWeight: 700,
            color: mode === "dark" ? "#fff" : "text.primary",
            letterSpacing: "0.02em",
            textAlign: "center", // középre igazítás
          }}
          aria-label="Projektek"
        >
          Projektek
        </Typography>
      </Box>
      <Box
        sx={{
          width: "100%",
          display: "flex",
          flexDirection: { xs: "column", sm: "row" },
          flexWrap: "wrap",
          gap: 3, // kisebb gap
          alignItems: { xs: "stretch", sm: "flex-start" },
          justifyContent: { xs: "center", sm: "flex-start" },
          px: { xs: 2, sm: 6 },
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
                // responsive flex-basis so cards wrap correctly across breakpoints
                flex: "1 1 260px",
                maxWidth: { xs: "100%", sm: 340, md: 320 },
                boxSizing: "border-box",
                width: "auto",
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
                    ? project.extra_images.map((img) => img.image_url || "").filter(Boolean)
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
    </Sheet>
  );
}

export default ProjectsPage;
