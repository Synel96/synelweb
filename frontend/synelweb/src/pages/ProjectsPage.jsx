import { useEffect, useState } from "react";
import { Box, Typography, Sheet } from "@mui/joy";
import ProjectsCard from "../components/projects/ProjectsCard";
import ProjectsSkeleton from "../components/projects/ProjectsSkeleton";
import { getProjects } from "../services/projectsService";
import { useColorScheme } from "@mui/joy/styles";
import NeonBackground from "../components/common/NeonBackground";

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
    <NeonBackground>
      <Sheet
        component="section"
        sx={{
          position: "relative",
          width: "100vw",
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          p: 0,
          m: 0,
          transition: "background 0.3s",
          background: "transparent",
        }}
        variant="plain"
        role="region"
        aria-label="Projektek oldal szekció"
        tabIndex={0}
      >
      
      {/* Cím - átlátszó háttérrel */}
      <Box
        sx={{
          position: "relative",
          zIndex: 2,
          mt: { xs: 4, sm: 6 },
          mb: 2,
          p: { xs: 2, sm: 3 },
          borderRadius: 4,
          bgcolor: mode === "dark" ? "rgba(18,18,18,0.85)" : "rgba(255,255,255,0.85)",
          backdropFilter: "blur(10px)",
          border: "2px solid",
          borderColor: "rgba(255,140,0,0.3)",
          boxShadow: "lg",
          width: { xs: "95%", sm: "80%", md: "auto" },
          maxWidth: "720px",
          mx: "auto",
          textAlign: "center",
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
      
      {/* Projektek konténer - Scrollable */}
      <Box
        sx={{
          width: "100%",
          display: "flex",
          flexDirection: { xs: "column", sm: "row" },
          flexWrap: "wrap",
          gap: 3,
          alignItems: "center",
          justifyContent: "center",
          px: { xs: 2, sm: 4, md: 6 },
          py: 4,
          position: "relative",
          zIndex: 2,
          minHeight: "50vh",
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
                width: "100%",
                maxWidth: { xs: "100%", sm: 520 },
                display: "flex",
                justifyContent: "center",
              }}
            >
              <ProjectsCard
                title={project.name}
                description={project.description}
                tags={project.slug ? [project.slug] : []}
                projectVideo={project.preview_video || ""}
                previewImage={project.preview_image || ""}
                previewImagePublicId={project.preview_image_public_id || ""}
                images={project.extra_images || []}
                link={project.link || ""}
                priority={idx === 0} // First project image gets priority for LCP
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
    </NeonBackground>
  );
}

export default ProjectsPage;
