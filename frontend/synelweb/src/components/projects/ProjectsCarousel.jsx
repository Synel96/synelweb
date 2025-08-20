import { useState } from "react";
import { Box, IconButton } from "@mui/joy";
import ArrowBack from "@mui/icons-material/ArrowBackIosNew";
import ArrowForward from "@mui/icons-material/ArrowForwardIos";
import ProjectMediaModal from "../modals/ProjectMediaModal"; // helyes import

function ProjectsCarousel({
  projectVideo = "",
  previewImage = "",
  images = [],
}) {
  const slides = [
    { type: "image", src: previewImage },
    { type: "video", src: projectVideo },
    ...images.map((img) => ({ type: "image", src: img })),
  ].filter((item) => !!item.src);

  const [current, setCurrent] = useState(0);
  const [modalOpen, setModalOpen] = useState(false);

  const goPrev = () =>
    setCurrent((prev) => (prev === 0 ? slides.length - 1 : prev - 1));
  const goNext = () =>
    setCurrent((prev) => (prev === slides.length - 1 ? 0 : prev + 1));

  if (slides.length === 0) {
    return (
      <Box
        sx={{
          width: "100%",
          maxWidth: 520,
          mx: "auto",
          py: 2,
          textAlign: "center",
        }}
        role="region"
        aria-label="Nincs megjeleníthető projekt média"
        tabIndex={0}
      >
        Nincs elérhető videó vagy kép ehhez a projekthez.
      </Box>
    );
  }

  return (
    <Box
      role="region"
      aria-label="Projekt körhinta"
      sx={{
        width: "100%",
        maxWidth: 520,
        mx: "auto",
        position: "relative",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        py: 2,
      }}
      tabIndex={0}
    >
      <Box
        sx={{
          width: "100%",
          aspectRatio: "16/9",
          borderRadius: 3,
          overflow: "hidden",
          boxShadow: "md",
          bgcolor: "background.level1",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          position: "relative",
          cursor: "pointer",
          transition: "box-shadow 0.3s, filter 0.3s",
          "&:hover": {
            boxShadow: "lg",
            filter: "brightness(0.95) drop-shadow(0 0 16px #90caf9)",
          },
          "&::after": {
            content: '"Nagyítás"',
            position: "absolute",
            right: 12,
            bottom: 12,
            background: "rgba(30,144,255,0.85)",
            color: "#fff",
            fontSize: "0.95rem",
            padding: "4px 12px",
            borderRadius: 16,
            opacity: 0,
            pointerEvents: "none",
            transition: "opacity 0.2s",
          },
          "&:hover::after": {
            opacity: 1,
          },
        }}
        aria-label={`Körhinta tartalom ${current + 1} / ${slides.length}`}
        tabIndex={0}
        onClick={() => setModalOpen(true)}
      >
        {slides[current].type === "video" ? (
          <video
            src={slides[current].src}
            controls
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
            aria-label="Projekt bemutató videó"
            tabIndex={0}
          />
        ) : (
          <img
            src={slides[current].src}
            alt={`Projekt kép ${current}`}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
            tabIndex={0}
          />
        )}
      </Box>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          width: "100%",
          mt: 2,
        }}
      >
        <IconButton aria-label="Előző elem" onClick={goPrev} tabIndex={0}>
          <ArrowBack />
        </IconButton>
        <Box
          sx={{
            display: "flex",
            gap: 1,
            alignItems: "center",
          }}
          aria-label="Körhinta navigáció"
        >
          {slides.map((_, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => setCurrent(idx)}
              style={{
                width: 18, // kisebb méret
                height: 18,
                borderRadius: "50%",
                background: idx === current ? "#ff9800" : "#ccc",
                border: "none",
                cursor: "pointer",
                outline: idx === current ? "2px solid #ff9800" : "none",
                transition: "all 0.2s",
                padding: 0,
                margin: 4,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
              aria-label={`Ugrás a(z) ${idx + 1}. elemre`}
            />
          ))}
        </Box>
        <IconButton aria-label="Következő elem" onClick={goNext} tabIndex={0}>
          <ArrowForward />
        </IconButton>
      </Box>
      {/* Modal hozzáadva */}
      <ProjectMediaModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        images={slides.filter((s) => s.type === "image").map((s) => s.src)}
        video={slides.find((s) => s.type === "video")?.src || ""}
      />
    </Box>
  );
}

export default ProjectsCarousel;
