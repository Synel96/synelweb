import { useColorScheme } from "@mui/joy";
import Sheet from "@mui/joy/Sheet";
import Box from "@mui/joy/Box";
import Typography from "@mui/joy/Typography";
import Button from "@mui/joy/Button";
import { Link } from "react-router-dom"; // React Router Link import
import reviewBg from "/review.png?w=1920&format=webp";

function ReviewSection() {
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
      aria-label="Értékelések szekció"
      tabIndex={0}
    >
      {/* Háttérkép lazy loadinggal */}
      <img
        src={reviewBg}
        alt="Értékelések háttérkép"
        loading="lazy"
        style={{
          position: "absolute",
          inset: 0,
          width: "100vw",
          height: "100%",
          objectFit: "cover",
          zIndex: 1,
          pointerEvents: "none",
        }}
        aria-hidden="true"
      />
      <Box
        sx={{
          position: "relative",
          zIndex: 2,
          backgroundColor:
            mode === "dark" ? "rgba(0,0,0,0.65)" : "rgba(255,255,255,0.85)",
          borderRadius: { xs: 2, sm: 3 },
          p: { xs: 2, sm: 4 },
          boxShadow: "md",
          maxWidth: 420,
          width: { xs: "95%", sm: "80%", md: "420px" },
          textAlign: "center",
          transition: "background 0.3s",
        }}
        role="region"
        aria-label="Értékelések tartalom"
        tabIndex={0}
      >
        <Typography
          level="h2"
          tabIndex={0}
          sx={{
            mb: 2,
            fontSize: { xs: "1.5rem", sm: "2.2rem" },
            color: mode === "dark" ? "#fff" : "#121212",
            fontWeight: 700,
            letterSpacing: "0.02em",
            transition: "color 0.3s",
          }}
        >
          Értékelje szolgáltatásunkat!
        </Typography>
        <Typography
          tabIndex={0}
          sx={{
            mb: 3,
            fontSize: { xs: "1rem", sm: "1.15rem" },
            color: mode === "dark" ? "#fff" : "#121212",
            fontWeight: 400,
            transition: "color 0.3s",
          }}
        >
          Fontos számunkra a véleménye! Kérjük, ossza meg tapasztalatát, és
          segítse munkánkat egy értékeléssel.
        </Typography>
        <Button
          size="lg"
          variant="solid"
          color="primary"
          sx={{
            fontWeight: 600,
            fontSize: "1.1rem",
            px: 3,
            py: 1.5,
            borderRadius: "8px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.10)",
            backgroundColor: "#ff9800",
            color: "#fff",
            "&:hover": {
              backgroundColor: "#ffb74d",
              color: "#fff",
            },
            transition: "background 0.2s",
          }}
          component={Link}
          to="/velemenyek" // ide irányít
          tabIndex={0}
          aria-label="Értékelés írása gomb"
        >
          Értékelés írása
        </Button>
      </Box>
    </Sheet>
  );
}

export default ReviewSection;
