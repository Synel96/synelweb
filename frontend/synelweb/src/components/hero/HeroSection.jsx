import { useColorScheme } from "@mui/joy";
import Sheet from "@mui/joy/Sheet";
import Box from "@mui/joy/Box";
import Typography from "@mui/joy/Typography";
import Button from "@mui/joy/Button";
import { Link } from "react-router-dom";
import Greet from "../greet/Greet";
import HeroInfoOverlay from "./HeroInfoOverlay";
import OptimizedBackgroundImage from "../common/OptimizedBackgroundImage";

function HeroSection() {
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
        transition: "background 0.3s",
      }}
      variant="plain"
      role="region"
      aria-label="Főoldal hős szekció"
      tabIndex={0}
    >
      {/* Cloudinary optimalizált háttérkép */}
      <OptimizedBackgroundImage
        cloudinaryId="hero_kfkbus"
        alt="Főoldal háttérkép"
        priority={true}
      />

      {/* Joy MUI overlay szekció */}
      <div
        className="hero-overlay"
        style={{
          position: "absolute",
          top: "10%",
          left: "50%",
          transform: "translateX(-50%)",
          width: "90%",
          zIndex: 2,
          background:
            mode === "dark" ? "rgba(0,0,0,0.65)" : "rgba(255,255,255,0.85)",
          borderRadius: "16px",
          padding: "1rem",
          boxShadow: "0 2px 16px rgba(0,0,0,0.15)",
        }}
      >
        <Greet />
      </div>

      {/* Info overlay Joy MUI */}
      <HeroInfoOverlay
        style={{
          position: "absolute",
          top: "60vh", // korábban: bottom: "50vh"
          left: "50%",
          transform: "translateX(-50%)",
          width: "min(90%, 1100px)",
          zIndex: 1,
        }}
      />

      <style>
        {`
          @media (max-width: 600px) {
            .hero-overlay {
              top: 0 !important;
              width: 100% !important;
              left: 50%;
              transform: translateX(-50%);
              border-radius: 0 0 16px 16px;
            }
            .hero-info-overlay {
              top: clamp(240px, 42vh, 520px) !important;
              bottom: auto !important;
              width: 80% !important;
              left: 50% !important;
              transform: translateX(-50%) !important;
              border-radius: 0 0 12px 12px;
            }
          }
        `}
      </style>
    </Sheet>
  );
}

export default HeroSection;
