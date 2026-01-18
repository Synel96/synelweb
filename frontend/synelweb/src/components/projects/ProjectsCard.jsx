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
  priority = false,
}) {
  const [expanded, setExpanded] = useState(false);
  const [descHeight, setDescHeight] = useState("auto");
  const shortDesc = (description || "").trim();
  const isLong = shortDesc.length > 220;

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
        position: "relative",
        cursor: "pointer",
        transition: "box-shadow 0.3s, border-color 0.3s, transform 0.3s",
        "&:hover": {
          boxShadow: "0 0 24px rgba(255,140,0,0.6)",
          borderColor: "rgba(255,140,0,0.8)",
          transform: "translateY(-4px)",
        },
      }}
      role="region"
      aria-label={`Projekt: ${title}`}
      tabIndex={0}
    >
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

      <Box>
        <Typography
          level="body2"
          sx={{
            color: "text.secondary",
            mb: 1,
            textAlign: "left",
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
              onClick={() => setExpanded((prev) => !prev)}
              aria-expanded={expanded}
            >
              {expanded ? "Kevesebb" : "Bővebben"}
            </Button>
          </Box>
        )}
      </Box>

      {tags && tags.length > 0 && (
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
      )}

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
