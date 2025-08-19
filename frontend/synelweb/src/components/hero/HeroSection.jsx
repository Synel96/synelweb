import { useColorScheme } from "@mui/joy";
import { useState, useEffect } from "react";
import Greet from "../greet/Greet";
import HeroInfoOverlay from "./HeroInfoOverlay";

function HeroSection() {
  const { mode } = useColorScheme();
  const [overlayVisible, setOverlayVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setOverlayVisible(true), 700);
    return () => clearTimeout(timer);
  }, []);

  return (
    <section
      aria-label="Főoldali üdvözlő szekció"
      role="region"
      tabIndex={0}
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: 0,
        textAlign: "center",
        minHeight: "600px",
        position: "relative",
        width: "100%",
      }}
    >
      <div
        style={{
          position: "relative",
          width: "100%",
          height: "100vh",
          minHeight: "600px",
          overflow: "hidden",
        }}
      >
        {/* Joy MUI Sheet a háttérhez, dark/light módra reagál */}
        <img
          src="/hero.webp"
          alt="Hero"
          loading="lazy"
          style={{
            position: "absolute",
            inset: 0,
            width: "100%",
            height: "100%",
            objectFit: "cover",
            borderRadius: 0,
            boxShadow: "0 4px 32px rgba(0,0,0,0.08)",
            zIndex: 1,
            filter: mode === "dark" ? "brightness(0.7)" : "none",
            transition: "filter 0.3s",
          }}
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
            opacity: overlayVisible ? 1 : 0,
            transition: "opacity 0.7s cubic-bezier(.4,0,.2,1), background 0.3s",
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
            pointerEvents: "none",
          }}
        />
      </div>

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
    </section>
  );
}

export default HeroSection;
