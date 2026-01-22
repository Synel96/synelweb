import { Box, Typography } from "@mui/joy";
import { useEffect, useState } from "react";
import PackagesCards from "../../components/packages/PackagesCards";
import PackagesSkeleton from "../../components/packages/PackagesSkeleton";
import { fetchPackages } from "../../services/packagesService";
import { useColorScheme } from "@mui/joy/styles";
import Warning from "../../components/packages/Warning";
import Sheet from "@mui/joy/Sheet";
import NeonBackground from "../../components/common/NeonBackground";

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
            aria-label="Szolgáltatások"
          >
            Szolgáltatások
          </Typography>
        </Box>

        {/* Kártyák konténer */}
        <Box
          sx={{
            width: "100%",
            display: "flex",
            flexDirection: { xs: "column", md: "row" },
            flexWrap: { xs: "nowrap", md: "wrap" },
            gap: { xs: 4, sm: 5, md: 6 },
            justifyContent: "center",
            alignItems: { xs: "center", md: "flex-start" },
            px: { xs: 2, sm: 4, md: 6 },
            py: 4,
            position: "relative",
            zIndex: 2,
            maxWidth: 1400,
            mx: "auto",
          }}
          role="region"
          aria-label="Szolgáltatáscsomagok listája"
        >
          {loading ? (
            <PackagesSkeleton count={3} />
          ) : (
            packages.map((pkg) => (
              <PackagesCards
                key={pkg.id}
                name={pkg.name}
                description={pkg.description}
                tags={pkg.tags}
                is_discounted={pkg.is_discounted}
                preview_image_url={pkg.preview_image_url}
                price={pkg.price}
                discounted_price={pkg.discounted_price}
              />
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
            from { opacity: 0; transform: translateY(20px); }
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
