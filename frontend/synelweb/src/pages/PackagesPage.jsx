import { Box, Typography } from "@mui/joy";
import { useEffect, useState } from "react";
import PackagesCards from "../components/packages/PackagesCards";
import PackagesSkeleton from "../components/packages/PackagesSkeleton";
import { fetchPackages } from "../services/packagesService";
import PercentIcon from "@mui/icons-material/Percent";
import { useColorScheme } from "@mui/joy/styles";
import Warning from "../components/packages/Warning";
import Sheet from "@mui/joy/Sheet";
import NeonBackground from "../components/common/NeonBackground";

function PackagesPage() {
  const [packages, setPackages] = useState([]);
  const [loading, setLoading] = useState(true);
  const { mode } = useColorScheme();

  useEffect(() => {
    fetchPackages()
      .then((res) => {
        const pkgs = Array.isArray(res.data)
          ? res.data.map((pkg) => ({
              ...pkg,
              tags: pkg.tags
                ? pkg.tags
                    .split(",")
                    .map((t) => t.trim())
                    .filter(Boolean)
                : [],
            }))
          : [];
        setPackages(pkgs);
      })
      .catch(() => setPackages([]))
      .finally(() => setLoading(false));
  }, []);

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
        aria-label="Csomagok oldal szekció"
        tabIndex={0}
      >
      {/* Cím */}
      <Box
        sx={{
          position: "relative",
          zIndex: 2,
          mt: { xs: 4, sm: 6 },
          mb: 2,
          p: { xs: 2, sm: 3 },
          borderRadius: 4,
          boxShadow: "md",
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
          aria-label="Szolgáltatások"
        >
          Szolgáltatások
        </Typography>
      </Box>

      {/* Kártyák konténer - Scrollable */}
      <Box
        sx={{
          width: "100%",
          display: "flex",
          flexWrap: "wrap",
          gap: { xs: 3, sm: 4, md: 6 },
          justifyContent: "center",
          alignItems: "flex-start",
          px: { xs: 2, sm: 4, md: 6 },
          py: 4,
          position: "relative",
          zIndex: 2,
          maxWidth: 1200,
          mx: "auto",
        }}
        role="region"
        aria-label="Szolgáltatáscsomagok listája"
      >
          {loading ? (
            <PackagesSkeleton count={3} />
          ) : (
            packages.map((pkg, idx) => (
              <Box
                key={pkg.id}
                sx={{
                  width: { xs: "100%", sm: "calc(50% - 16px)", md: "360px" },
                  display: "flex",
                  flexDirection: "column",
                  alignSelf: "flex-start", // <-- fontos!
                  gap: 2,
                  position: "relative",
                  transition: "box-shadow 0.3s, filter 0.3s, transform 0.2s",
                  opacity: 0,
                  animation: `fadeInUp 0.7s cubic-bezier(.4,0,.2,1) ${
                    0.25 + idx * 0.12
                  }s forwards`,
                  boxShadow: "0 2px 8px rgba(0,0,0,0.10)",
                  borderRadius: 2,
                  backgroundColor:
                    mode === "dark" ? "rgba(24,24,24,0.92)" : "#fff",
                  "&:hover": {
                    boxShadow: "0 8px 24px rgba(0,0,0,0.15)",
                    filter: "brightness(0.99)",
                    transform: "translateY(-2px)",
                  },
                }}
                role="article"
                aria-label={`Csomag: ${pkg.name}`}
              >
                {/* % ikon */}
                {pkg.is_discounted && (
                  <Box
                    sx={{
                      position: "absolute",
                      top: 8,
                      right: 12,
                      zIndex: 3,
                      background: "#ff9800",
                      color: "#fff",
                      borderRadius: "50%",
                      width: 36,
                      height: 36,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      boxShadow: "0 2px 8px rgba(0,0,0,0.10)",
                      animation:
                        "percentPulse 1.8s infinite cubic-bezier(.4,0,.2,1)",
                    }}
                    aria-label="Akciós csomag"
                  >
                    <PercentIcon fontSize="small" sx={{ color: "#ff1744" }} />
                    <style>
                      {`
                        @keyframes percentPulse {
                          0% {
                            transform: scale(1) translateY(0);
                            box-shadow: 0 0 0 0 #ff9800;
                          }
                          50% {
                            transform: scale(1.18) translateY(-4px);
                            box-shadow: 0 0 16px 8px #ff9800;
                          }
                          100% {
                            transform: scale(1) translateY(0);
                            box-shadow: 0 0 0 0 #ff9800;
                          }
                        }
                      `}
                    </style>
                  </Box>
                )}

                {/* A kártya tartalma */}
                <PackagesCards
                  name={pkg.name}
                  description={pkg.description}
                  tags={pkg.tags}
                  is_discounted={pkg.is_discounted}
                  preview_image_url={pkg.preview_image_url}
                  price={pkg.price}
                  discounted_price={pkg.discounted_price}
                />
              </Box>
            ))
          )}
        </Box>

        {/* Figyelmeztetés */}
        <Box
          sx={{
            width: "100%",
            display: "flex",
            justifyContent: "center",
            px: { xs: 2, sm: 4 },
            pb: 4,
          }}
        >
          <Warning
            sx={{
              position: "relative",
              zIndex: 2,
              width: { xs: "100%", sm: "80%", md: 520 },
              maxWidth: "720px",
            }}
          />
        </Box>

      {/* Animációk */}
      <style>
        {`
          @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(28px); }
            to { opacity: 1; transform: translateY(0); }
          }
          @keyframes fadeInBg {
            from { opacity: 0; }
            to { opacity: 1; }
          }
        `}
      </style>
    </Sheet>
    </NeonBackground>
  );
}

export default PackagesPage;
