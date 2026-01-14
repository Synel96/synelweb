import { Box, IconButton } from "@mui/joy";
import useDarkMode from "../../hooks/useDarkMode";
import Menu from "./Menu";
import useMediaQuery from "@mui/material/useMediaQuery";
import Logo from "./Logo";

function Navbar() {
  const { mode, setMode } = useDarkMode();
  // Dark mode: világos logó kell (#121212 sötét háttéren)
  // Light mode: sötét logó kell (#fff világos háttéren)
  const logoSrc = mode === "dark" ? "/lightlogo.svg" : "/darklogo.svg";
  const isMobile = useMediaQuery("(max-width:600px)");

  return (
    <Box
      component="header"
      sx={{
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: isMobile ? "center" : "space-between",
        px: 3,
        py: 2,
        bgcolor: mode === "dark" ? "#121212" : "#fff",
        borderBottom: "none",
        position: "relative",
      }}
      role="banner"
      aria-label="Fő navigációs sáv"
    >
      <Box
        sx={{ display: "flex", alignItems: "center" }}
        role="region"
        aria-label="Weboldal logó"
      >
        <Logo src={logoSrc} isMobile={isMobile} />
      </Box>

      {!isMobile && (
        <Box
          sx={{ display: "flex", alignItems: "center" }}
          role="navigation"
          aria-label="Főmenü"
        >
          <Menu />
        </Box>
      )}

      <IconButton
        variant="soft"
        aria-label={
          mode === "dark"
            ? "Világos mód bekapcsolása"
            : "Sötét mód bekapcsolása"
        }
        onClick={() => setMode(mode === "dark" ? "light" : "dark")}
        sx={{
          position: isMobile ? "absolute" : "static",
          right: isMobile ? 16 : "auto",
          zIndex: 3,
        }}
      >
        {mode === "dark" ? "🌞" : "🌙"}
      </IconButton>

      {isMobile && (
        <Box
          sx={{ position: "absolute", left: 16, zIndex: 3 }}
          role="navigation"
          aria-label="Mobilmenü"
        >
          <Menu />
        </Box>
      )}
    </Box>
  );
}

export default Navbar;
