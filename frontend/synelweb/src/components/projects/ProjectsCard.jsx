import { Box, Typography, Chip, Button } from "@mui/joy";
import ProjectsCarousel from "./ProjectsCarousel";

function ProjectsCard({
  title,
  description,
  tags = [],
  projectVideo,
  previewImage,
  images = [],
  link,
}) {
  return (
    <Box
      sx={{
        width: "100%",
        maxWidth: 520,
        bgcolor: "background.level1",
        borderRadius: 4,
        boxShadow: "md",
        p: { xs: 2, sm: 3 },
        mb: 4,
        display: "flex",
        flexDirection: "column",
        gap: 2,
        transition:
          "box-shadow 0.5s cubic-bezier(.4,0,.2,1), filter 0.5s cubic-bezier(.4,0,.2,1)",
        "&:hover": {
          boxShadow: "lg",
          filter: "drop-shadow(0 0 24px #90caf9)",
        },
      }}
      role="region"
      aria-label={`Projekt kártya: ${title}`}
      tabIndex={0}
    >
      <ProjectsCarousel
        projectVideo={projectVideo}
        previewImage={previewImage}
        images={images}
      />
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
      <Typography
        level="body2"
        sx={{
          color: "text.secondary",
          mb: 1,
          textAlign: "left",
        }}
      >
        {description}
      </Typography>
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
          size="md" // kisebb gomb
          sx={{
            mt: 1,
            fontWeight: 700,
            fontSize: "1rem",
            px: 2.5,
            py: 1,
            borderRadius: 3,
            backgroundColor: "#ff9800", // narancssárga
            color: "#212121", // sötét szöveg, WCAG-kompatibilis
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
