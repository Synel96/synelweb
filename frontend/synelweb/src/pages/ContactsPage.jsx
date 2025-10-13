import { useColorScheme } from "@mui/joy/styles";
import Sheet from "@mui/joy/Sheet";
import Box from "@mui/joy/Box";
import Typography from "@mui/joy/Typography";
import Contacts from "../components/contactspage/Contacts";
import contactPageBg from "/contactpage.png?w=1920&format=webp";

function ContactsPage() {
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
      aria-label="Kapcsolat oldal szekció"
      tabIndex={0}
    >
      {/* Háttérkép lazy loadinggal */}
      <img
        src={contactPageBg}
        alt="Kapcsolat oldal háttérkép"
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
      {/* Elérhetőség cím és box */}
      <Box
        sx={{
          position: "relative",
          zIndex: 2,
          backgroundColor:
            mode === "dark" ? "rgba(30,30,30,0.92)" : "rgba(255,255,255,0.85)",
          borderRadius: 4,
          p: { xs: 2, sm: 4 },
          boxShadow: "md",
          maxWidth: 420,
          width: { xs: "95%", sm: "80%", md: "420px" },
          textAlign: "center",
          mt: { xs: 4, sm: 6 },
          opacity: 0,
          transform: "translateY(32px)",
          animation: "fadeInUp 0.8s cubic-bezier(.4,0,.2,1) 0.1s forwards",
        }}
      >
        <Typography
          level="h1"
          sx={{
            mb: 2,
            fontSize: { xs: "2rem", sm: "2.5rem" },
            color: mode === "dark" ? "#fff" : "#121212",
            fontWeight: 700,
            letterSpacing: "0.02em",
            textAlign: "center",
            opacity: 0,
            animation: "fadeInUp 0.8s cubic-bezier(.4,0,.2,1) 0.2s forwards",
          }}
          tabIndex={0}
        >
          Elérhetőség
        </Typography>
      </Box>
      {/* Contacts komponens külön, animáltan */}
      <Box
        sx={{
          position: "relative",
          zIndex: 2,
          width: "100%",
          maxWidth: 420,
          mt: 3,
          opacity: 0,
          transform: "translateY(32px)",
          animation: "fadeInUp 0.8s cubic-bezier(.4,0,.2,1) 0.6s forwards",
        }}
      >
        <Contacts />
      </Box>
      {/* Animációs kulcsszavak */}
      <style>
        {`
          @keyframes fadeInUp {
            from {
              opacity: 0;
              transform: translateY(32px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
          @keyframes fadeInBg {
            from {
              opacity: 0;
            }
            to {
              opacity: 1;
            }
          }
        `}
      </style>
    </Sheet>
  );
}

export default ContactsPage;
