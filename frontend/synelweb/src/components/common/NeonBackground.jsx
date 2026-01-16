import { Box } from "@mui/joy";
import { useColorScheme } from "@mui/joy/styles";

function NeonBackground({ children, sx = {} }) {
  const { mode } = useColorScheme();

  return (
    <Box
      sx={{
        position: "relative",
        width: "100%",
        minHeight: "100vh",
        ...sx,
      }}
    >
      {/* Neon narancssárga háttér réteg */}
      <Box
        sx={{
          position: "fixed",
          top: 0,
          left: 0,
          width: "100vw",
          height: "100vh",
          zIndex: -1,
          pointerEvents: "none",
          overflow: "hidden",
        }}
      >
        {/* Fő narancssárga gradiens */}
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: "120%",
            height: "120%",
            background:
              mode === "dark"
                ? "radial-gradient(ellipse at center, rgba(255,140,0,0.15) 0%, rgba(255,69,0,0.08) 35%, transparent 70%)"
                : "radial-gradient(ellipse at center, rgba(255,165,0,0.12) 0%, rgba(255,140,0,0.06) 35%, transparent 70%)",
            filter: "blur(60px)",
            animation: "neonPulse 8s ease-in-out infinite",
          }}
        />

        {/* Második réteg - élénkebb középpont */}
        <Box
          sx={{
            position: "absolute",
            top: "40%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: "80%",
            height: "80%",
            background:
              mode === "dark"
                ? "radial-gradient(circle, rgba(255,140,0,0.2) 0%, rgba(255,100,0,0.1) 25%, transparent 50%)"
                : "radial-gradient(circle, rgba(255,165,0,0.15) 0%, rgba(255,140,0,0.08) 25%, transparent 50%)",
            filter: "blur(80px)",
            animation: "neonPulse 6s ease-in-out infinite reverse",
          }}
        />

        {/* Harmadik réteg - alsó neon fény */}
        <Box
          sx={{
            position: "absolute",
            bottom: "10%",
            left: "30%",
            width: "60%",
            height: "60%",
            background:
              mode === "dark"
                ? "radial-gradient(ellipse, rgba(255,100,0,0.18) 0%, rgba(255,69,0,0.09) 30%, transparent 60%)"
                : "radial-gradient(ellipse, rgba(255,140,0,0.12) 0%, rgba(255,100,0,0.06) 30%, transparent 60%)",
            filter: "blur(70px)",
            animation: "neonPulse 10s ease-in-out infinite",
          }}
        />

        {/* Negyedik réteg - felső kiegészítő */}
        <Box
          sx={{
            position: "absolute",
            top: "15%",
            right: "20%",
            width: "50%",
            height: "50%",
            background:
              mode === "dark"
                ? "radial-gradient(circle, rgba(255,120,0,0.15) 0%, rgba(255,80,0,0.08) 25%, transparent 50%)"
                : "radial-gradient(circle, rgba(255,150,0,0.1) 0%, rgba(255,120,0,0.05) 25%, transparent 50%)",
            filter: "blur(90px)",
            animation: "neonPulse 7s ease-in-out infinite",
          }}
        />
      </Box>

      {/* Tartalom */}
      {children}

      {/* Animációk */}
      <style>
        {`
          @keyframes neonPulse {
            0%, 100% {
              opacity: 1;
              transform: translate(-50%, -50%) scale(1);
            }
            50% {
              opacity: 0.85;
              transform: translate(-50%, -50%) scale(1.05);
            }
          }
        `}
      </style>
    </Box>
  );
}

export default NeonBackground;
