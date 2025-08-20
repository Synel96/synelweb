import { Box, Typography, Modal } from "@mui/joy";

function PrivacyPolicyModal({ open, onClose }) {
  return (
    <Modal
      open={open}
      onClose={onClose}
      aria-labelledby="privacy-policy-title"
      aria-describedby="privacy-policy-desc"
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1300,
      }}
    >
      <Box
        sx={{
          maxWidth: { xs: "98vw", sm: 500, md: 650 },
          width: "100%",
          maxHeight: { xs: "90vh", sm: "80vh" },
          overflowY: "auto",
          p: { xs: 2, sm: 4 },
          backgroundColor: "background.surface",
          borderRadius: 4,
          boxShadow: "lg",
          outline: "none",
          color: "text.primary",
        }}
        role="document"
        tabIndex={-1}
        aria-modal="true"
      >
        <Typography
          id="privacy-policy-title"
          level="h1"
          sx={{
            mb: 2,
            fontWeight: 700,
            fontSize: { xs: "1.5rem", sm: "2rem" },
            lineHeight: 1.2,
          }}
        >
          Adatvédelmi tájékoztató
        </Typography>
        <Typography id="privacy-policy-desc" sx={{ mb: 2 }}>
          Ez az oldal tiszteletben tartja a felhasználók személyes adatait, és
          elkötelezett azok védelme mellett. Az alábbiakban tájékoztatjuk Önt
          arról, hogy milyen adatokat kezelünk, milyen célból, és hogyan
          gondoskodunk azok biztonságáról.
        </Typography>
        <Typography
          level="h2"
          sx={{
            mt: 2,
            mb: 1,
            fontWeight: 600,
            fontSize: { xs: "1.1rem", sm: "1.25rem" },
            lineHeight: 1.3,
          }}
        >
          1. Kezelt adatok köre
        </Typography>
        <Typography sx={{ mb: 1 }}>
          Az oldal használata során az alábbi személyes adatokat kérhetjük
          Öntől:
        </Typography>
        <Box
          component="ul"
          sx={{
            pl: 3,
            mb: 2,
            fontSize: "1rem",
            color: "text.primary",
            "& li": {
              marginBottom: "4px",
              lineHeight: 1.5,
            },
          }}
        >
          <li>Név</li>
          <li>E-mail cím</li>
          <li>Vélemény, üzenet szövege</li>
        </Box>
        <Typography sx={{ mb: 2 }}>
          Ezeket az adatokat kizárólag az Ön hozzájárulásával, a vélemények
          megjelenítése, kapcsolattartás vagy válaszadás céljából kezeljük.
        </Typography>
        <Typography
          level="h2"
          sx={{
            mt: 2,
            mb: 1,
            fontWeight: 600,
            fontSize: { xs: "1.1rem", sm: "1.25rem" },
            lineHeight: 1.3,
          }}
        >
          2. Adatkezelés célja
        </Typography>
        <Typography sx={{ mb: 2 }}>
          Az adatokat kizárólag a szolgáltatás működtetése, a felhasználói
          vélemények megjelenítése, illetve az Önnel való kapcsolatfelvétel
          céljából kezeljük. Az adatokat harmadik félnek nem adjuk át, kivéve
          jogszabályi kötelezettség esetén.
        </Typography>
        <Typography
          level="h2"
          sx={{
            mt: 2,
            mb: 1,
            fontWeight: 600,
            fontSize: { xs: "1.1rem", sm: "1.25rem" },
            lineHeight: 1.3,
          }}
        >
          3. Adatbiztonság
        </Typography>
        <Typography sx={{ mb: 2 }}>
          Az Ön adatait bizalmasan kezeljük, és minden szükséges technikai és
          szervezési intézkedést megteszünk azok védelme érdekében.
        </Typography>
        <Typography
          level="h2"
          sx={{
            mt: 2,
            mb: 1,
            fontWeight: 600,
            fontSize: { xs: "1.1rem", sm: "1.25rem" },
            lineHeight: 1.3,
          }}
        >
          4. Jogai az adatkezeléssel kapcsolatban
        </Typography>
        <Typography sx={{ mb: 2 }}>
          Ön jogosult tájékoztatást kérni az Önről kezelt adatokról, kérheti
          azok helyesbítését, törlését, valamint tiltakozhat az adatkezelés
          ellen. Kérését az oldal üzemeltetőjének elérhetőségén keresztül
          jelezheti.
        </Typography>
        <Typography
          level="h2"
          sx={{
            mt: 2,
            mb: 1,
            fontWeight: 600,
            fontSize: { xs: "1.1rem", sm: "1.25rem" },
            lineHeight: 1.3,
          }}
        >
          5. Kapcsolat
        </Typography>
        <Typography sx={{ mb: 2 }}>
          Adatkezelő: Németh Szilveszter
          <br />
          E-mail: info@synelweb.hu
        </Typography>
        <Typography
          sx={{
            mt: 4,
            fontSize: "0.95rem",
            color: "text.secondary",
            textAlign: "right",
          }}
        >
          Utolsó frissítés: 2025. augusztus 20.
        </Typography>
        <Box sx={{ textAlign: "right", mt: 2 }}>
          <button
            type="button"
            onClick={onClose}
            style={{
              background: "#eee",
              color: "#121212",
              border: "none",
              borderRadius: "6px",
              padding: "8px 16px",
              fontWeight: 600,
              cursor: "pointer",
            }}
            aria-label="Bezárás"
          >
            Bezár
          </button>
        </Box>
      </Box>
    </Modal>
  );
}

export default PrivacyPolicyModal;
