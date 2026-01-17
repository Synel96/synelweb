import { useColorScheme } from "@mui/joy";
import Typography from "@mui/joy/Typography";
import Sheet from "@mui/joy/Sheet";
import Button from "@mui/joy/Button";
import { Link } from "react-router-dom";
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
          fontSize: { xs: "0.9rem", sm: "1.15rem" },
          color: mode === "dark" ? "#fff" : "#121212",
          mb: { xs: 2, sm: 3 },
        }}
      >
        Böngésszen szolgáltatásaink között, vagy ismerd meg jobban a munkámat!
      </Typography>

      <Button
        component={Link}
        to="/rolam"
        size="lg"
        sx={{
          bgcolor: "#e65100",
          color: "#fff",
          fontWeight: 600,
          fontSize: { xs: "1rem", sm: "1.1rem" },
          px: { xs: 3, sm: 4 },
          py: { xs: 1.5, sm: 2 },
          borderRadius: 3,
          boxShadow: "0 4px 14px rgba(230,81,0,0.4)",
          transition: "all 0.3s cubic-bezier(.4,0,.2,1)",
          "&:hover": {
            bgcolor: "#bf360c",
            boxShadow: "0 6px 20px rgba(230,81,0,0.6)",
            transform: "translateY(-2px)",
          },
          "&:active": {
            transform: "translateY(0)",
          },
        }}
      >
        Tudj meg többet Rólam és a Munkámról
      </Button>
    </Sheet>
  );
}

export default HeroInfoOverlay;
