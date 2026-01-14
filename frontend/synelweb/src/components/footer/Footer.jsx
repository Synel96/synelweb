import { Box, Typography, Link } from "@mui/joy";
import { useState } from "react";
import PrivacyPolicyModal from "../modals/PrivacyPolicyModal"; // helyes import

function Footer() {
  const [openPolicy, setOpenPolicy] = useState(false);

  return (
    <>
      <Box
        component="footer"
        sx={{
          width: "100%",
          bgcolor: "background.body",
          color: "text.primary",
          py: 3,
          mt: 6,
          minHeight: "120px",
          textAlign: "center",
          borderTop: "1px solid #eee",
        }}
        role="contentinfo"
        aria-label="Oldal lábléc"
      >
        <Typography level="body2">
          © {new Date().getFullYear()} Synel Web Solutions | Minden jog
          fenntartva.
        </Typography>
        <Box sx={{ mt: 1 }}>
          <Link
            component="button"
            onClick={() => setOpenPolicy(true)}
            sx={{ fontSize: "1rem", fontWeight: 500 }}
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
