import { useState } from "react";
import { Box, Typography, Chip, Button } from "@mui/joy";
import ProjectsCarousel from "./ProjectsCarousel";

function ProjectsCard({
  title,
  description,
  tags = [],
  projectVideo,
  previewImage,
  previewImagePublicId,
  images = [],
  link,
  priority = false, // Add priority prop for LCP optimization
}) {
  const [expanded, setExpanded] = useState(false);
  const shortDesc = (description || "").trim();
  const isLong = shortDesc.length > 220; // ha hosszabb, akkor rövidítjük

  return (
    <Box
      sx={{
        width: "100%",
        maxWidth: { xs: "100%", sm: 520 },
        bgcolor: "background.surface",
        borderRadius: 4,
        boxShadow: "lg",
        border: "2px solid",
        borderColor: "divider",
        p: { xs: 2, sm: 3 },
        mb: 4,
        display: "flex",
        flexDirection: "column",
        gap: 2,
        transition:
          "box-shadow 0.5s cubic-bezier(.4,0,.2,1), filter 0.5s cubic-bezier(.4,0,.2,1), border-color 0.3s",
        "&:hover": {
          boxShadow: "xl",
          filter: "drop-shadow(0 0 24px rgba(255,140,0,0.4))",
          borderColor: "rgba(255,140,0,0.5)",
        },
      }}
      role="region"
      aria-label={`Projekt kártya: ${title}`}
      tabIndex={0}
    >
      {/* Title first */}
      <Typography
        level="h2"
        sx={{
          fontSize: { xs: "1.3rem", sm: "1.7rem" },
          fontWeight: 700,
          color: "text.primary",
          mb: 1,
          textAlign: "left",
        }}
        aria-label={`Projekt neve: ${title}`}
        tabIndex={0}
      >
        {title}
      </Typography>

      <ProjectsCarousel
        projectVideo={projectVideo}
        previewImage={previewImage}
        previewImagePublicId={previewImagePublicId}
        images={images}
        priority={priority}
      />
      {/* Leírás - összecsukható */}
      <Box>
        <Typography
          level="body2"
          sx={{
            color: "text.secondary",
            mb: 1,
            textAlign: "left",
            // ha nincs kinyitva, alkalmazzuk a line-clamp stílust
            display: expanded ? "block" : "-webkit-box",
            WebkitLineClamp: expanded ? undefined : 4,
            WebkitBoxOrient: expanded ? undefined : "vertical",
            overflow: expanded ? "visible" : "hidden",
          }}
        >
          {shortDesc}
        </Typography>

        {isLong && (
          <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
            <Button
              variant="plain"
              size="sm"
              onClick={() => setExpanded((s) => !s)}
              aria-expanded={expanded}
            >
              {expanded ? "Kevesebb" : "Bővebben"}
            </Button>
          </Box>
        )}
      </Box>

      <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap", mb: 1 }}>
        {tags.map((tag, idx) => (
          <Chip
            key={idx}
            color="primary"
            variant="soft"
            sx={{ fontSize: "0.95rem" }}
            aria-label={`Címke: ${tag}`}
            tabIndex={0}
          >
            {tag}
          </Chip>
        ))}
      </Box>
      {link && (
        <Button
          component="a"
          href={link}
          target="_blank"
          rel="noopener noreferrer"
          variant="solid"
          color="warning"
          size="md"
          sx={{
            mt: 1,
            fontWeight: 700,
            fontSize: "1rem",
            px: 2.5,
            py: 1,
            borderRadius: 3,
            backgroundColor: "#ff9800",
            color: "#212121",
            "&:hover": {
              backgroundColor: "#fb8c00",
              color: "#212121",
            },
            boxShadow: "sm",
          }}
          aria-label="Projekt megtekintése"
          tabIndex={0}
        >
          Projekt megtekintése
        </Button>
      )}
    </Box>
  );
}

export default ProjectsCard;
