import { Box, Typography } from "@mui/joy";

function Footer() {
  return (
    <Box
      component="footer"
      sx={{
        width: "100%",
        bgcolor: "background.body",
        color: "text.primary",
        py: 3,
        mt: 6,
        textAlign: "center",
        borderTop: "1px solid #eee",
      }}
    >
      <Typography level="body2">
        © {new Date().getFullYear()} Synel Web Solutions | Minden jog
        fenntartva.
      </Typography>
    </Box>
  );
}

export default Footer;
