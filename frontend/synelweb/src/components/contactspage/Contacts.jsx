import { Box, Typography, Button, Stack, useColorScheme } from "@mui/joy";
import EmailIcon from "@mui/icons-material/Email";
import LinkedInIcon from "@mui/icons-material/LinkedIn";
import LocationOnIcon from "@mui/icons-material/LocationOn";

function Contacts() {
  const { mode } = useColorScheme();
  const btnBaseSx = {
    width: "100%",
    fontWeight: 600,
    transition: "background-color 0.18s ease, color 0.18s ease",
    "&:hover": {
      backgroundColor: "#1976d2",
      color: "#fff",
    },
  };
  const desc = `Az alábbi címeken és linkeken keresztül érhet el bennünket, és kérhet akár online vagy személyes megbeszélést Sopronban.`;

  return (
    <Box
      component="section"
      sx={{
        width: "100%",
        maxWidth: 420,
        mx: "auto",
        mt: { xs: 2, sm: 4 },
        mb: { xs: 2, sm: 4 },
        p: { xs: 2, sm: 4 },
        borderRadius: 4,
        backgroundColor:
          mode === "dark" ? "rgba(30,30,30,0.95)" : "rgba(255,255,255,0.95)",
        textAlign: "center",
        display: "flex",
        flexDirection: "column",
        gap: 3,
        transition: "box-shadow 0.3s",
        boxShadow: "md",
        "&:hover": {
          boxShadow:
            "0 0 32px 8px rgba(30, 136, 229, 0.25), 0 2px 8px rgba(0,0,0,0.10)",
        },
      }}
      role="region"
      aria-label="Elérhetőségi információk"
      tabIndex={0}
    >
      <Typography
        level="body2"
        sx={{
          color: mode === "dark" ? "#fff" : "text.secondary",
          mb: 2,
        }}
        tabIndex={0}
      >
        {desc}
      </Typography>

      <Stack direction="column" spacing={2} alignItems="center">
        <Button
          component="a"
          href="mailto:info@synelweb.hu"
          startDecorator={<EmailIcon />}
          variant="soft"
          color="primary"
          sx={btnBaseSx}
          aria-label="E-mail küldése: info@synelweb.hu"
        >
          info@synelweb.hu
        </Button>
        <Button
          component="a"
          href="https://www.linkedin.com/in/szilveszter-nemeth-636689332/"
          target="_blank"
          rel="noopener noreferrer"
          startDecorator={<LinkedInIcon />}
          variant="soft"
          color="neutral"
          sx={btnBaseSx}
          aria-label="LinkedIn profil megnyitása"
        >
          LinkedIn profil
        </Button>
        <Button
          component="a"
          href="https://www.google.com/maps/place/Sopron/"
          target="_blank"
          rel="noopener noreferrer"
          startDecorator={<LocationOnIcon />}
          variant="soft"
          color="success"
          sx={btnBaseSx}
          aria-label="Google Térkép - Sopron"
        >
          Sopron (Google Térkép)
        </Button>
      </Stack>
    </Box>
  );
}

export default Contacts;
