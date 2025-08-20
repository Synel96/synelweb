import { extendTheme } from "@mui/joy";

const theme = extendTheme({
  fontFamily: {
    body: '"Inter", "Roboto", "Arial", sans-serif',
    display: '"Inter", "Roboto", "Arial", sans-serif',
  },
  colorSchemes: {
    light: {
      palette: {
        primary: { solidBg: "#1976d2", solidHoverBg: "#1565c0" },
        secondary: { solidBg: "#00bfae" },
        background: { body: "#fff" },
      },
    },
    dark: {
      palette: {
        primary: { solidBg: "#90caf9", solidHoverBg: "#64b5f6" },
        secondary: { solidBg: "#00bfae" },
        background: { body: "#121212" },
      },
    },
  },
  radius: {
    sm: "8px",
    md: "16px",
    lg: "24px",
  },
  typography: {
    h1: { fontSize: "2.5rem", fontWeight: 700 },
    h2: { fontSize: "2rem", fontWeight: 700 },
    body1: { fontSize: "1rem" },
  },
});

export default theme;