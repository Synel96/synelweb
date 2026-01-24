import { useState, useEffect, useRef } from "react";
import { useColorScheme } from "@mui/joy";
import Typography from "@mui/joy/Typography";
import Box from "@mui/joy/Box";
import Sheet from "@mui/joy/Sheet";

function Greet() {
  const [greetVisible, setGreetVisible] = useState(false);
  const [descVisible, setDescVisible] = useState(false);
  const [waveOnce, setWaveOnce] = useState(false);
  const { mode } = useColorScheme();
  const intervalRef = useRef();

  useEffect(() => {
    const greetTimer = setTimeout(() => setGreetVisible(true), 700);
    const descTimer = setTimeout(() => setDescVisible(true), 1400);

    // Induló integetés
    const waveTimer = setTimeout(() => setWaveOnce(true), 800);
    const waveEndTimer = setTimeout(() => setWaveOnce(false), 2000);

    // 5 mp-enként újrainduló integetés
    intervalRef.current = setInterval(() => {
      setWaveOnce(true);
      setTimeout(() => setWaveOnce(false), 1200);
    }, 5000);

    return () => {
      clearTimeout(greetTimer);
      clearTimeout(descTimer);
      clearTimeout(waveTimer);
      clearTimeout(waveEndTimer);
      clearInterval(intervalRef.current);
    };
  }, []);

  return (
    <Sheet
      variant="plain"
      suppressHydrationWarning
      sx={{
        textAlign: "center",
        boxShadow: "none",
        background: "none",
        p: { xs: 1, sm: 2, md: 3 },
        m: 0,
        width: "100%",
        maxWidth: 700,
        mx: "auto",
      }}
      role="region"
      aria-labelledby="greet-heading greet-desc"
      tabIndex={0}
    >
      <Box>
        <Typography
          id="greet-heading"
          level="h1"
          sx={{
            opacity: greetVisible ? 1 : 0,
            transform: greetVisible ? "translateY(0)" : "translateY(32px)",
            transition:
              "opacity 0.7s cubic-bezier(.4,0,.2,1), transform 0.7s cubic-bezier(.4,0,.2,1)",
            fontSize: { xs: "1.5rem", sm: "2rem", md: "2.75rem" },
            fontWeight: 700,
            fontFamily: '"Inter", "Roboto", "Arial", sans-serif',
            letterSpacing: "0.02em",
            lineHeight: 1.3,
            textShadow:
              mode === "dark"
                ? "0 2px 12px rgba(0,0,0,0.7)"
                : "0 2px 12px rgba(255,255,255,0.7)",
            color: mode === "dark" ? "#fff" : "#121212",
            m: 0,
            display: "inline-block",
          }}
        >
          Üdvözöllek a SynelWeb-en!
          <Box
            component="span"
            sx={{
              marginLeft: "0.5rem",
              fontSize: { xs: "1.5rem", sm: "2rem", md: "2.75rem" },
              display: "inline-block",
              animation: waveOnce ? "wave 1.2s" : "none",
              transformOrigin: "70% 70%",
            }}
          >
            👋
          </Box>
          <style>
            {`
              @keyframes wave {
                0% { transform: rotate(0deg); }
                15% { transform: rotate(20deg); }
                30% { transform: rotate(-10deg); }
                40% { transform: rotate(20deg); }
                50% { transform: rotate(-4deg); }
                60% { transform: rotate(10deg); }
                100% { transform: rotate(0deg); }
              }
            `}
          </style>
        </Typography>
        <Typography
          id="greet-desc"
          level="body-lg"
          sx={{
            opacity: descVisible ? 1 : 0,
            transform: descVisible ? "translateY(0)" : "translateY(32px)",
            transition:
              "opacity 0.7s cubic-bezier(.4,0,.2,1) 0.2s, transform 0.7s cubic-bezier(.4,0,.2,1) 0.2s",
            fontSize: { xs: "0.875rem", sm: "1rem", md: "1.2rem" },
            mt: { xs: 1.5, sm: 2 },
            color: mode === "dark" ? "#fff" : "#121212",
            maxWidth: 600,
            fontWeight: 400,
            lineHeight: 1.5,
            mx: "auto",
          }}
        >
          Teljes körű webfejlesztés, dizájn, hosting és mobilbarát megoldások
          egy helyen!
        </Typography>
      </Box>
    </Sheet>
  );
}

export default Greet;
