import { useColorScheme } from "@mui/joy";
import { useState, useEffect } from "react";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";

function HeroInfoOverlay(props) {
  const { mode } = useColorScheme();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setVisible(true), 2200);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div
      className="hero-info-overlay"
      style={{
        ...props.style, // pozicionálás kívülről
        margin: "0 auto",
        display: "block",
        background:
          mode === "dark" ? "rgba(0,0,0,0.55)" : "rgba(255,255,255,0.92)",
        borderRadius: "12px",
        padding: "0.75rem 1rem",
        boxShadow: "0 2px 12px rgba(0,0,0,0.10)",
        opacity: visible ? 1 : 0,
        transition: "opacity 0.7s cubic-bezier(.4,0,.2,1)",
        fontSize: "clamp(1rem, 2vw, 1.15rem)",
        color: mode === "dark" ? "#fff" : "#121212",
        fontWeight: 500,
        textAlign: "center",
      }}
    >
      Böngésszen szolgáltatásaink között, vagy görgessen lejjebb további
      információkért!
      <div
        style={{
          marginTop: "1rem",
          display: "flex",
          justifyContent: "center",
        }}
      >
        <ArrowDownwardIcon
          sx={{
            fontSize: 36,
            color: mode === "dark" ? "#fff" : "#121212",
            animation: "bounce 1.2s infinite",
          }}
        />
        <style>
          {`
            @keyframes bounce {
              0%, 100% { transform: translateY(0); }
              50% { transform: translateY(12px); }
            }
          `}
        </style>
      </div>
    </div>
  );
}

export default HeroInfoOverlay;
