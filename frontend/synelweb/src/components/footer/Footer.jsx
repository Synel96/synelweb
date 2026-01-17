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
          py: { xs: 3, sm: 3 },
          mt: 6,
          height: { xs: "140px", sm: "120px" }, // Fix height to prevent CLS
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          textAlign: "center",
          borderTop: "1px solid #eee",
        }}
        role="contentinfo"
        aria-label="Oldal lábléc"
      >
        <Typography 
          level="body2"
          sx={{
            fontSize: { xs: "0.875rem", sm: "0.875rem" },
            lineHeight: 1.5,
          }}
        >
          © {new Date().getFullYear()} Synel Web Solutions | Minden jog
          fenntartva.
        </Typography>
        <Box sx={{ mt: 1 }}>
          <Link
            component="button"
            onClick={() => setOpenPolicy(true)}
            sx={{ 
              fontSize: { xs: "0.875rem", sm: "1rem" },
              fontWeight: 500,
              lineHeight: 1.5,
            }}
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
