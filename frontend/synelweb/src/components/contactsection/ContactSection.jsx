import { useColorScheme } from "@mui/joy";
import Button from "@mui/joy/Button";
import Sheet from "@mui/joy/Sheet";
import Typography from "@mui/joy/Typography";
import Box from "@mui/joy/Box";
import { Link } from "react-router-dom";

function ContactSection() {
  const { mode } = useColorScheme();

  return (
    <Sheet
      component="section"
      sx={{
        position: "relative",
        width: "100%",
        minHeight: { xs: 400, sm: 500, md: 600 },
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        overflow: "hidden",
        p: 0,
      }}
      variant="plain"
      role="region"
      aria-label="Kapcsolat szekció"
      tabIndex={0}
    >
      <img
        src="/contact.webp"
        alt="Kapcsolat háttérkép"
        loading="lazy"
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
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
        }}
        role="region"
        aria-label="Kapcsolat tartalom"
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
          }}
        >
          Lépjen velünk kapcsolatba!
        </Typography>
        <Typography
          tabIndex={0}
          sx={{
            mb: 3,
            fontSize: { xs: "1rem", sm: "1.15rem" },
            color: mode === "dark" ? "#fff" : "#121212",
            fontWeight: 400,
          }}
        >
          Kérdése van, ajánlatot szeretne vagy visszahívást kérne? Küldje el
          nekünk üzenetét!
        </Typography>
        <Button
          size="lg"
          variant="solid"
          component={Link}
          to="/elerhetoseg"
          sx={{
            fontWeight: 600,
            fontSize: "1.1rem",
            px: 3,
            py: 1.5,
            borderRadius: "8px",
            boxShadow: "0 2px 8px rgba(255,140,0,0.15)",
            backgroundColor: "#ff9800",
            color: "#fff",
            "&:hover": {
              backgroundColor: "#ffb74d",
              color: "#fff",
            },
            transition: "background 0.2s",
          }}
          tabIndex={0}
          aria-label="Kapcsolatfelvétel gomb"
        >
          Kapcsolatfelvétel
        </Button>
      </Box>
    </Sheet>
  );
}

export default ContactSection;
