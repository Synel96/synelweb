import { Box, Typography } from "@mui/joy";
import { useEffect, useState } from "react";
import PackagesCards from "../components/packages/PackagesCards";
import PackagesSkeleton from "../components/packages/PackagesSkeleton";
import { fetchPackages } from "../services/packagesService";
import PercentIcon from "@mui/icons-material/Percent";
import { useColorScheme } from "@mui/joy/styles";

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
    <Box
      component="main"
      sx={{
        width: "100%",
        minHeight: "80vh",
        position: "relative",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "flex-start",
        overflow: "hidden",
        p: { xs: 2, sm: 4 },
      }}
      role="main"
      aria-label="Szolgáltatások oldal"
      tabIndex={0}
    >
      {/* Animált háttérkép */}
      <img
        src="/packagespage.webp"
        alt=""
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
          zIndex: 1,
          pointerEvents: "none",
          opacity: 0,
          animation: "fadeInBg 1s cubic-bezier(.4,0,.2,1) 0.05s forwards",
        }}
        aria-hidden="true"
      />
      {/* Cím */}
      <Box
        sx={{
          position: "relative",
          zIndex: 2,
          mt: { xs: 4, sm: 6 },
          mb: 2,
          p: { xs: 2, sm: 4 },
          borderRadius: 4,
          backgroundColor:
            mode === "dark" ? "rgba(30,30,30,0.85)" : "rgba(255,255,255,0.85)",
          boxShadow: "md",
          width: { xs: "95%", sm: "80%", md: "420px" },
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
            color: mode === "dark" ? "#fff" : "#121212",
            letterSpacing: "0.02em",
            textAlign: "center",
          }}
          aria-label="Szolgáltatások"
        >
          Szolgáltatások
        </Typography>
      </Box>
      {/* Kártyák */}
      {loading ? (
        <PackagesSkeleton count={3} />
      ) : (
        <Box
          sx={{
            width: "100%",
            maxWidth: 1200,
            mx: "auto",
            zIndex: 2,
            display: "flex",
            flexWrap: "wrap",
            gap: 3,
            justifyContent: { xs: "center", sm: "flex-start" },
            alignItems: "stretch",
            alignContent: "flex-start",
          }}
          role="region"
          aria-label="Szolgáltatáscsomagok listája"
        >
          {packages.map((pkg, idx) => (
            <Box
              key={pkg.id}
              sx={{
                maxWidth: 340,
                minWidth: 260,
                flex: "1 1 320px",
                display: "flex",
                flexDirection: "column",
                gap: 2,
                position: "relative",
                // mb: 0, // nincs alsó margó, hogy az animáció illeszkedjen
                transition: "box-shadow 0.3s, filter 0.3s",
                opacity: 0,
                animation: `fadeInUp 0.7s cubic-bezier(.4,0,.2,1) ${
                  0.3 + idx * 0.15
                }s forwards${
                  pkg.is_discounted
                    ? ", discountPulse 1.8s infinite cubic-bezier(.4,0,.2,1)"
                    : ""
                }`,
                boxShadow: pkg.is_discounted
                  ? "0 0 32px 12px #ff9800"
                  : "0 2px 8px rgba(0,0,0,0.10)",
                "&:hover": {
                  boxShadow: pkg.is_discounted
                    ? "0 0 40px 16px #ff9800"
                    : "0 4px 16px rgba(0,0,0,0.15)",
                  filter: "brightness(0.98)",
                },
                borderRadius: 12,
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
                    width: 32,
                    height: 32,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    boxShadow: "0 2px 8px rgba(0,0,0,0.10)",
                    animation:
                      "discountPulse 1.8s infinite cubic-bezier(.4,0,.2,1)",
                  }}
                >
                  <PercentIcon fontSize="small" />
                </Box>
              )}
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
          ))}
        </Box>
      )}
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
          @keyframes fadeInBg {
            from {
              opacity: 0;
            }
            to {
              opacity: 1;
            }
          }
          @keyframes discountPulse {
            0% {
              box-shadow: 0 0 0 0 #ff9800;
              transform: scale(1);
            }
            50% {
              box-shadow: 0 0 32px 12px #ff9800;
              transform: scale(1.06);
            }
            100% {
              box-shadow: 0 0 0 0 #ff9800;
              transform: scale(1);
            }
          }
        `}
      </style>
    </Box>
  );
}

export default PackagesPage;
