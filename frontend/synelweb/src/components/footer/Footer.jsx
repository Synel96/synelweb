import { Box, Typography, Link } from "@mui/joy";
import { useState, useEffect } from "react";
import PrivacyPolicyModal from "../modals/PrivacyPolicyModal";

function Footer() {
  const [openPolicy, setOpenPolicy] = useState(false);
  const [year, setYear] = useState("");

  useEffect(() => {
    setYear(new Date().getFullYear());
  }, []);

  return (
    <>
      <Box
        component="footer"
        sx={{
          width: "100%",
          bgcolor: "background.body",
          color: "text.primary",
          py: { xs: 3, sm: 3 },
          mt: 6,
          height: { xs: "140px", sm: "120px" },
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          textAlign: "center",
          borderTop: "1px solid #eee",
          flexShrink: 0,
        }}
        role="contentinfo"
        aria-label="Oldal lábléc"
      >
        <Typography
          level="body2"
          sx={{
            fontSize: { xs: "0.875rem", sm: "0.875rem" },
            lineHeight: 1.5,
            fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
            fontWeight: 400,
          }}
        >
          © {year || "2026"} Synel Web Solutions | Minden jog fenntartva.
        </Typography>
        <Box sx={{ mt: 1, mb: 1, display: "flex", flexWrap: "wrap", gap: 2, justifyContent: "center" }}>
          <Link href="/" sx={{ fontSize: "0.95rem", fontWeight: 500 }}>Főoldal</Link>
          <Link href="/projektek" sx={{ fontSize: "0.95rem", fontWeight: 500 }}>Projektek</Link>
          <Link href="/velemenyek" sx={{ fontSize: "0.95rem", fontWeight: 500 }}>Vélemények</Link>
          <Link href="/szolgaltatasok" sx={{ fontSize: "0.95rem", fontWeight: 500 }}>Szolgáltatások</Link>
          <Link href="/elerhetoseg" sx={{ fontSize: "0.95rem", fontWeight: 500 }}>Elérhetőség</Link>
          <Link href="/rolam" sx={{ fontSize: "0.95rem", fontWeight: 500 }}>Rólam</Link>
          <Link
            component="button"
            onClick={() => setOpenPolicy(true)}
            sx={{ fontSize: "0.95rem", fontWeight: 500 }}
            aria-label="Adatvédelmi tájékoztató megnyitása"
          >
            Adatvédelmi tájékoztató
          </Link>
        </Box>
      </Box>
      <PrivacyPolicyModal
        open={openPolicy}
        onClose={() => setOpenPolicy(false)}
      />
    </>
  );
}

export default Footer;
