import React from "react";
import { useColorScheme } from "@mui/joy";
import Sheet from "@mui/joy/Sheet";
import Box from "@mui/joy/Box";
import Typography from "@mui/joy/Typography";
import Button from "@mui/joy/Button";
import { Link } from "react-router-dom";
import OptimizedBackgroundImage from "../common/OptimizedBackgroundImage";

function ProjectsSection() {
  const { mode } = useColorScheme();

  return (
    <Sheet
      component="section"
      sx={{
        position: "relative",
        width: "100vw",
        minHeight: { xs: "60vw", sm: "60vw", md: "60vw" },
        maxHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        overflow: "hidden",
        p: 0,
        m: 0,
        mb: { xs: 4, sm: 6, md: 8 },
        transition: "background 0.3s",
      }}
      variant="plain"
      role="region"
      aria-label="Projektek szekció"
      tabIndex={0}
    >
      {/* Cloudinary optimalizált háttérkép */}
      <OptimizedBackgroundImage 
        cloudinaryId="projects_plkitq"
        alt="Projektek háttérkép"
      />
      <Box
        sx={{
          position: "relative",
          zIndex: 2,
          backgroundColor:
            mode === "dark" ? "rgba(0,0,0,0.65)" : "rgba(255,255,255,0.85)",
          borderRadius: { xs: 2, sm: 3 },
          p: { xs: 2, sm: 4 },
          boxShadow: "md",
          maxWidth: { xs: 420, md: 520 },
          width: { xs: "95%", sm: "85%", md: "520px" },
          textAlign: "center",
          transition: "background 0.3s",
        }}
        role="region"
        aria-label="Projektek tartalom"
        tabIndex={0}
      >
        <Typography
          level="h2"
          tabIndex={0}
          sx={{
            mb: 2,
            fontSize: { xs: "1.5rem", sm: "2.2rem" },
            color: mode === "dark" ? "#fff" : "#121212",
            fontWeight: 700,
            letterSpacing: "0.02em",
            transition: "color 0.3s",
          }}
        >
          Tekintsd meg projektjeimet!
        </Typography>
        <Typography
          tabIndex={0}
          sx={{
            mb: 3,
            fontSize: { xs: "1rem", sm: "1.15rem" },
            color: mode === "dark" ? "#fff" : "#121212",
            fontWeight: 400,
            transition: "color 0.3s",
          }}
        >
          Ismerd meg eddigi munkáimat és referenciáimat!
        </Typography>
        <Button
          size="lg"
          variant="solid"
          color="primary"
          sx={{
            fontWeight: 600,
            fontSize: "1.1rem",
            px: 3,
            py: 1.5,
            borderRadius: "8px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.10)",
            backgroundColor: "#e65100", // Darker orange for better contrast (7.78:1)
            color: "#fff",
            "&:hover": {
              backgroundColor: "#f57c00", // Lighter on hover but still accessible (5.88:1)
              color: "#fff",
            },
            transition: "background 0.2s",
          }}
          component={Link}
          to="/projektek"
          tabIndex={0}
          aria-label="Projektek megtekintése gomb"
        >
          Projektek megtekintése
        </Button>
      </Box>
    </Sheet>
  );
}

export default ProjectsSection;
