import { Box, IconButton } from "@mui/joy";
import useDarkMode from "../../hooks/useDarkMode";
import Menu from "./Menu";
import useMediaQuery from "@mui/material/useMediaQuery";
import Logo from "./Logo";

function Navbar() {
  const { mode, setMode } = useDarkMode();
  const logoSrc = mode === "light" ? "/darklogo.png" : "/lightlogo.png";
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
    >
      <Logo src={logoSrc} isMobile={isMobile} />

      {!isMobile && <Menu />}
      <IconButton
        variant="soft"
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
        <Box sx={{ position: "absolute", left: 16, zIndex: 3 }}>
          <Menu />
        </Box>
      )}
    </Box>
  );
}

export default Navbar;
