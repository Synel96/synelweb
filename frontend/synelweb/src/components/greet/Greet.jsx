import { useState, useEffect } from "react";
import { useColorScheme } from "@mui/joy";

function Greet() {
  const [greetVisible, setGreetVisible] = useState(false);
  const [descVisible, setDescVisible] = useState(false);
  const { mode } = useColorScheme();

  useEffect(() => {
    const greetTimer = setTimeout(() => setGreetVisible(true), 700);
    const descTimer = setTimeout(() => setDescVisible(true), 1400);
    return () => {
      clearTimeout(greetTimer);
      clearTimeout(descTimer);
    };
  }, []);

  return (
    <div style={{ textAlign: "center" }}>
      <h1
        style={{
          opacity: greetVisible ? 1 : 0,
          transform: greetVisible ? "translateY(0)" : "translateY(32px)",
          transition:
            "opacity 0.7s cubic-bezier(.4,0,.2,1), transform 0.7s cubic-bezier(.4,0,.2,1)",
          fontSize: "clamp(1.5rem, 6vw, 2.5rem)",
          fontWeight: 700,
          fontFamily: '"Inter", "Roboto", "Arial", sans-serif',
          letterSpacing: "0.02em",
          lineHeight: 1.2,
          textShadow:
            mode === "dark"
              ? "0 2px 12px rgba(0,0,0,0.7)"
              : "0 2px 12px rgba(255,255,255,0.7)",
          color: mode === "dark" ? "#fff" : "#121212",
          margin: 0,
          display: "inline-block",
        }}
      >
        Üdvözöljük a Synel Web Solutions oldalán
        <span
          style={{
            marginLeft: "0.5rem",
            fontSize: "clamp(1.5rem, 6vw, 2.5rem)",
            display: "inline-block",
            animation: greetVisible ? "wave 1.2s infinite" : "none",
            transformOrigin: "70% 70%",
          }}
        >
          👋
        </span>
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
      </h1>
      <p
        style={{
          opacity: descVisible ? 1 : 0,
          transform: descVisible ? "translateY(0)" : "translateY(32px)",
          transition:
            "opacity 0.7s cubic-bezier(.4,0,.2,1) 0.2s, transform 0.7s cubic-bezier(.4,0,.2,1) 0.2s",
          fontSize: "clamp(1rem, 3vw, 1.25rem)",
          margin: "1.5rem auto 0 auto",
          color: mode === "dark" ? "#fff" : "#121212",
          maxWidth: 600,
          fontWeight: 400,
          lineHeight: 1.5,
        }}
      >
        Teljes körű webfejlesztés, dizájn, hosting és mobilbarát megoldások egy
        helyen!
      </p>
    </div>
  );
}

export default Greet;
