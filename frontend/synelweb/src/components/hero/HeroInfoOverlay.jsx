import { useColorScheme } from "@mui/joy";
import Typography from "@mui/joy/Typography";
import Sheet from "@mui/joy/Sheet";
import { useState, useEffect } from "react";

function HeroInfoOverlay(props) {
  const { mode } = useColorScheme();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setVisible(true), 2200);
    return () => {
      clearTimeout(timer);
    };
  }, []);

  return (
    <Sheet
      className="hero-info-overlay"
      role="region"
      aria-labelledby="hero-info-desc"
      tabIndex={0}
      sx={{
        ...props.style,
        margin: "0 auto",
        display: "block",
        backgroundColor:
          mode === "dark" ? "rgba(0,0,0,0.55)" : "rgba(255,255,255,0.92)",
        borderRadius: { xs: 2, sm: 3 },
        p: { xs: 2, sm: 3 },
        boxShadow: "md",
        maxWidth: 600,
        width: { xs: "95%", sm: "80%", md: "600px" },
        textAlign: "center",
        opacity: visible ? 1 : 0,
        transition: "opacity 0.7s cubic-bezier(.4,0,.2,1), background 0.3s",
      }}
      variant="plain"
    >
      <Typography
        id="hero-info-desc"
        level="body-lg"
        sx={{
          fontWeight: 500,
          fontSize: { xs: "1rem", sm: "1.15rem" },
          color: mode === "dark" ? "#fff" : "#121212",
        }}
      >
        Böngésszen szolgáltatásaink között, vagy görgessen lejjebb további
        információkért!
      </Typography>
      {/* Nyíl és animáció teljesen eltávolítva */}
    </Sheet>
  );
}

export default HeroInfoOverlay;
