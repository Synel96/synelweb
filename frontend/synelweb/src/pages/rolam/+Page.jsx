import {
  Box,
  Typography,
  Sheet,
  Accordion,
  AccordionDetails,
  AccordionSummary,
} from "@mui/joy";
import { useColorScheme } from "@mui/joy/styles";
import NeonBackground from "../../components/common/NeonBackground";

function AboutPage() {
  const { mode } = useColorScheme();

  return (
    <NeonBackground>
      <Sheet
        component="section"
        sx={{
          position: "relative",
          width: "100vw",
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          p: 0,
          m: 0,
          transition: "background 0.3s",
          background: "transparent",
        }}
        variant="plain"
        role="region"
        aria-label="Rólam oldal szekció"
        tabIndex={0}
      >
        {/* Cím */}
        <Box
          sx={{
            position: "relative",
            zIndex: 2,
            mt: { xs: 4, sm: 6 },
            mb: { xs: 4, sm: 6, md: 8 },
            p: { xs: 2, sm: 3 },
            borderRadius: 4,
            bgcolor:
              mode === "dark"
                ? "rgba(18,18,18,0.85)"
                : "rgba(255,255,255,0.85)",
            backdropFilter: "blur(10px)",
            border: "2px solid",
            borderColor: "rgba(255,140,0,0.3)",
            boxShadow: "lg",
            width: { xs: "95%", sm: "80%", md: "auto" },
            maxWidth: "720px",
            mx: "auto",
            textAlign: "center",
            opacity: 0,
            animation: "fadeInUp 0.7s cubic-bezier(.4,0,.2,1) 0.1s forwards",
          }}
        >
          <Typography
            level="h1"
            tabIndex={0}
            sx={{
              fontSize: { xs: "2rem", sm: "2.5rem", md: "3rem" },
              fontWeight: 700,
              color: mode === "dark" ? "#fff" : "text.primary",
              letterSpacing: "0.02em",
              textAlign: "center",
            }}
            aria-label="Rólam"
          >
            Rólam
          </Typography>
        </Box>

        {/* Tartalom */}
        <Box
          sx={{
            width: "100%",
            maxWidth: 900,
            mx: "auto",
            px: { xs: 2, sm: 4, md: 6 },
            py: 4,
            position: "relative",
            zIndex: 2,
          }}
        >
          <Box
            sx={{
              bgcolor: "background.surface",
              borderRadius: 4,
              border: "2px solid",
              borderColor: "divider",
              boxShadow: "lg",
              p: { xs: 4, sm: 5, md: 6 }, // Increased padding
              opacity: 0,
              animation: "fadeInUp 0.7s cubic-bezier(.4,0,.2,1) 0.3s forwards",
            }}
          >
            <Typography
              level="title-lg"
              sx={{
                color: "text.primary",
                fontWeight: 600,
                lineHeight: 1.6,
                mb: 3,
              }}
            >
              Szia, Szilveszter vagyok!
            </Typography>

            <Typography
              level="body-lg"
              sx={{
                color: "text.secondary",
                lineHeight: 1.8,
              }}
            >
              Több mint egy éve foglalkozom webfejlesztéssel, azon belül is
              modern, nagyvállalati környezetben is bizonyított technológiákkal.
              Olyan rendszerekkel dolgozom, amelyeket olyan cégek használnak, mint
              a Facebook, Instagram, Pinterest, vagy akár a NASA adminisztrációs
              rendszerei.
            </Typography>
          </Box>

          {/* Accordion Section */}
          <Box
            sx={{
              mt: { xs: 4, sm: 6 },
              display: "flex",
              flexDirection: "column",
              gap: 3,
            }}
          >
            {/* Accordion 1 */}
            <Accordion
              sx={{
                bgcolor: "background.surface",
                borderRadius: 4,
                border: "2px solid",
                borderColor: "divider",
                boxShadow: "lg",
                opacity: 0,
                animation:
                  "fadeInUp 0.7s cubic-bezier(.4,0,.2,1) 0.5s forwards",
                "& .MuiAccordionSummary-root": {
                  px: { xs: 3, sm: 4 },
                  py: { xs: 2, sm: 2.5 },
                },
                "& .MuiAccordionDetails-root": {
                  px: { xs: 3, sm: 4 },
                  py: { xs: 2, sm: 3 },
                },
              }}
            >
              <AccordionSummary>
                <Typography level="title-lg" sx={{ fontWeight: 600 }}>
                  Mit csinál egy jó weboldal valójában?
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography
                  level="body-md"
                  sx={{ color: "text.secondary", lineHeight: 1.8, mb: 2 }}
                >
                  Egy jó weboldal nem csak jelen van, hanem dolgozik helyetted.
                  Nem egy online névjegykártya, hanem a branded aktív része:
                </Typography>
                <Box
                  component="ul"
                  sx={{ pl: 3, color: "text.secondary", lineHeight: 1.8 }}
                >
                  <li>képes eladni,</li>
                  <li>növeli a forgalmad,</li>
                  <li>segíti az ügyfeleiddel való kapcsolattartást,</li>
                  <li>és leveszi a válladról a repetitív feladatokat.</li>
                </Box>
                <Typography
                  level="body-md"
                  sx={{ color: "text.secondary", lineHeight: 1.8, mt: 2 }}
                >
                  Egy jól megtervezett weboldal olyan, mint egy megbízható
                  munkatárs, aki 0–24-ben érted dolgozik.
                </Typography>
              </AccordionDetails>
            </Accordion>

            {/* Accordion 2 */}
            <Accordion
              sx={{
                bgcolor: "background.surface",
                borderRadius: 4,
                border: "2px solid",
                borderColor: "divider",
                boxShadow: "lg",
                opacity: 0,
                animation:
                  "fadeInUp 0.7s cubic-bezier(.4,0,.2,1) 0.6s forwards",
                "& .MuiAccordionSummary-root": {
                  px: { xs: 3, sm: 4 },
                  py: { xs: 2, sm: 2.5 },
                },
                "& .MuiAccordionDetails-root": {
                  px: { xs: 3, sm: 4 },
                  py: { xs: 2, sm: 3 },
                },
              }}
            >
              <AccordionSummary>
                <Typography level="title-lg" sx={{ fontWeight: 600 }}>
                  Miért engem válassz?
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography
                  level="body-md"
                  sx={{ color: "text.secondary", lineHeight: 1.8, mb: 2 }}
                >
                  Hiszem, hogy megfizethető áron is lehet:
                </Typography>
                <Box
                  component="ul"
                  sx={{
                    pl: 3,
                    color: "text.secondary",
                    lineHeight: 1.8,
                    mb: 2,
                  }}
                >
                  <li>szép,</li>
                  <li>modern,</li>
                  <li>és villámgyors weboldalt készíteni.</li>
                </Box>
                <Typography
                  level="body-md"
                  sx={{ color: "text.secondary", lineHeight: 1.8, mb: 2 }}
                >
                  Nem sablonokat árulok, hanem egyedi megoldásokat. Közösen
                  megkeressük a számodra és a vállalkozásod számára
                  legmegfelelőbb irányt, majd erre építjük fel a rendszert.
                </Typography>
                <Typography
                  level="body-md"
                  sx={{ color: "text.secondary", lineHeight: 1.8, mb: 2 }}
                >
                  Az általam használt technológiáknak és
                  teljesítmény-optimalizálásnak köszönhetően a végeredmény:
                </Typography>
                <Box
                  component="ul"
                  sx={{ pl: 3, color: "text.secondary", lineHeight: 1.8 }}
                >
                  <li>
                    lényegesen gyorsabb, mint egy átlagos tartalomkezelővel
                    (WordPress, Shopify) készült oldal,
                  </li>
                  <li>
                    különösen mobilon, ami kulcsfontosságú, hiszen a látogatók
                    70–80%-a telefonról érkezik.
                  </li>
                </Box>
              </AccordionDetails>
            </Accordion>

            {/* Accordion 3 */}
            <Accordion
              sx={{
                bgcolor: "background.surface",
                borderRadius: 4,
                border: "2px solid",
                borderColor: "divider",
                boxShadow: "lg",
                opacity: 0,
                animation:
                  "fadeInUp 0.7s cubic-bezier(.4,0,.2,1) 0.7s forwards",
                "& .MuiAccordionSummary-root": {
                  px: { xs: 3, sm: 4 },
                  py: { xs: 2, sm: 2.5 },
                },
                "& .MuiAccordionDetails-root": {
                  px: { xs: 3, sm: 4 },
                  py: { xs: 2, sm: 3 },
                },
              }}
            >
              <AccordionSummary>
                <Typography level="title-lg" sx={{ fontWeight: 600 }}>
                  Egyedi admin felület, korlátok nélkül
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography
                  level="body-md"
                  sx={{ color: "text.secondary", lineHeight: 1.8, mb: 2 }}
                >
                  Az admin felületet egyedileg alakítjuk ki, így bármilyen
                  dinamikus funkció megvalósítható, például:
                </Typography>
                <Box
                  component="ul"
                  sx={{ pl: 3, color: "text.secondary", lineHeight: 1.8 }}
                >
                  <li>időpontfoglalás,</li>
                  <li>online portfólió vagy galéria,</li>
                  <li>kapcsolatfelvételi űrlapok,</li>
                  <li>rendelésleadás vagy egyedi üzleti logika.</li>
                </Box>
              </AccordionDetails>
            </Accordion>

            {/* Accordion 4 */}
            <Accordion
              sx={{
                bgcolor: "background.surface",
                borderRadius: 4,
                border: "2px solid",
                borderColor: "divider",
                boxShadow: "lg",
                opacity: 0,
                animation:
                  "fadeInUp 0.7s cubic-bezier(.4,0,.2,1) 0.8s forwards",
                "& .MuiAccordionSummary-root": {
                  px: { xs: 3, sm: 4 },
                  py: { xs: 2, sm: 2.5 },
                },
                "& .MuiAccordionDetails-root": {
                  px: { xs: 3, sm: 4 },
                  py: { xs: 2, sm: 3 },
                },
              }}
            >
              <AccordionSummary>
                <Typography level="title-lg" sx={{ fontWeight: 600 }}>
                  Teljes körű szolgáltatás
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography
                  level="body-md"
                  sx={{ color: "text.secondary", lineHeight: 1.8, mb: 2 }}
                >
                  A weboldal mellett az alábbiakat is biztosítani tudom:
                </Typography>
                <Box
                  component="ul"
                  sx={{ pl: 3, color: "text.secondary", lineHeight: 1.8 }}
                >
                  <li>teljes körű frontend és backend fejlesztés,</li>
                  <li>Neon / PostgreSQL adatbázis,</li>
                  <li>
                    felhőalapú képtárolás automatikus, performance-optimalizált
                    konvertálással,
                  </li>
                  <li>domain és tárhely ügyintézés,</li>
                  <li>céges e-mailek, SMTP és automatikus e-mail küldés,</li>
                  <li>Google Business beállítás,</li>
                  <li>alap SEO és technikai optimalizálás.</li>
                </Box>
              </AccordionDetails>
            </Accordion>

            {/* Accordion 5 */}
            <Accordion
              sx={{
                bgcolor: "background.surface",
                borderRadius: 4,
                border: "2px solid",
                borderColor: "divider",
                boxShadow: "lg",
                opacity: 0,
                animation:
                  "fadeInUp 0.7s cubic-bezier(.4,0,.2,1) 0.9s forwards",
                "& .MuiAccordionSummary-root": {
                  px: { xs: 3, sm: 4 },
                  py: { xs: 2, sm: 2.5 },
                },
                "& .MuiAccordionDetails-root": {
                  px: { xs: 3, sm: 4 },
                  py: { xs: 2, sm: 3 },
                },
              }}
            >
              <AccordionSummary>
                <Typography level="title-lg" sx={{ fontWeight: 600 }}>
                  Hogyan zajlik egy projekt?
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Box
                  component="ol"
                  sx={{ pl: 3, color: "text.secondary", lineHeight: 1.8 }}
                >
                  <li>Közös egyeztetés és specifikáció készítése</li>
                  <li>Látványterv a megbeszéltek alapján</li>
                  <li>Projekt kickoff, fejlesztés megkezdése</li>
                  <li>
                    Teljesítmény- és SEO-optimalizálás mobilra és asztalra
                  </li>
                  <li>
                    Domain, céges e-mailek és Google-beállítások összekötése
                  </li>
                  <li>Átadás</li>
                </Box>
              </AccordionDetails>
            </Accordion>

            {/* Accordion 6 */}
            <Accordion
              sx={{
                bgcolor: "background.surface",
                borderRadius: 4,
                border: "2px solid",
                borderColor: "divider",
                boxShadow: "lg",
                opacity: 0,
                animation:
                  "fadeInUp 0.7s cubic-bezier(.4,0,.2,1) 1.0s forwards",
                "& .MuiAccordionSummary-root": {
                  px: { xs: 3, sm: 4 },
                  py: { xs: 2, sm: 2.5 },
                },
                "& .MuiAccordionDetails-root": {
                  px: { xs: 3, sm: 4 },
                  py: { xs: 2, sm: 3 },
                },
              }}
            >
              <AccordionSummary>
                <Typography level="title-lg" sx={{ fontWeight: 600 }}>
                  Munkamódszer
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography
                  level="body-md"
                  sx={{ color: "text.secondary", lineHeight: 1.8 }}
                >
                  Agilis szemléletben dolgozom, ahol a folyamatos kommunikáció
                  kulcsfontosságú. Ez biztosítja, hogy a végeredmény pontosan
                  olyan weboldal legyen, amilyet elképzeltél – kompromisszumok
                  nélkül.
                </Typography>
              </AccordionDetails>
            </Accordion>

            {/* Accordion 7 */}
            <Accordion
              sx={{
                bgcolor: "background.surface",
                borderRadius: 4,
                border: "2px solid",
                borderColor: "divider",
                boxShadow: "lg",
                opacity: 0,
                animation:
                  "fadeInUp 0.7s cubic-bezier(.4,0,.2,1) 1.1s forwards",
                "& .MuiAccordionSummary-root": {
                  px: { xs: 3, sm: 4 },
                  py: { xs: 2, sm: 2.5 },
                },
                "& .MuiAccordionDetails-root": {
                  px: { xs: 3, sm: 4 },
                  py: { xs: 2, sm: 3 },
                },
              }}
            >
              <AccordionSummary>
                <Typography level="title-lg" sx={{ fontWeight: 600 }}>
                  Weboldalak helyi vállalkozásoknak és közösségeknek
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography
                  level="body-md"
                  sx={{ color: "text.secondary", lineHeight: 1.8, mb: 2 }}
                >
                  A SynelWeb olyan weboldalakat készít, amelyek érthetők,
                  gyorsak és könnyen használhatók – akár egy kisvállalkozásról,
                  egy településről vagy egy magánprojektről van szó.
                </Typography>
                <Typography
                  level="body-md"
                  sx={{ color: "text.secondary", lineHeight: 1.8, mb: 2 }}
                >
                  A közös munka során arra törekszem, hogy az elkészült weboldal
                  valóban segítse a mindennapokat: megkönnyítse a
                  kapcsolattartást, bemutassa a fontos információkat, és
                  elérhetővé tegye azt, amit az emberek keresnek.
                </Typography>
                <Typography
                  level="body-md"
                  sx={{ color: "text.secondary", lineHeight: 1.8, mb: 2 }}
                >
                  Mivel a munkám jelentős része Sopronban és a környező
                  településeken zajlik, pontosan ismerem a helyi igényeket, és
                  ehhez igazítom a weboldalak felépítését és működését. Az
                  oldalak mobilon is jól használhatók, átláthatók, és hosszú
                  távon is megbízható alapot adnak.
                </Typography>
                <Typography
                  level="body-md"
                  sx={{ color: "text.secondary", lineHeight: 1.8 }}
                >
                  A fejlesztés során személyesen és online is elérhető vagyok,
                  így a folyamat végén egy olyan weboldalt kapsz, amely nem túl
                  bonyolult, nem túlmagyarázott, hanem egyszerűen teszi a
                  dolgát.
                </Typography>
              </AccordionDetails>
            </Accordion>
          </Box>
        </Box>

        {/* Animációk */}
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
          `}
        </style>
      </Sheet>
    </NeonBackground>
  );
}

export default AboutPage;
