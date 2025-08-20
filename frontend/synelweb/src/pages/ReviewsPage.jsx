import { Box, Typography, useColorScheme } from "@mui/joy";
import ReviewsCarousel from "../components/reviews/ReviewsCarousel";
import CreateReviewButton from "../components/reviews/CreateReviewButton";
import { useEffect, useState } from "react";
import { fetchReviews } from "../services/reviewsService";
import SuccessSnackbar from "../components/modals/SucessSnackbar";
import ReviewsSkeleton from "../components/reviews/ReviewsSkeleton";

function ReviewsPage() {
  const { mode } = useColorScheme();
  const [reviews, setReviews] = useState([]);
  const [showSuccess, setShowSuccess] = useState(false);
  const [loading, setLoading] = useState(true); // új állapot

  // Frissítés sikeres beküldés után
  const refreshReviews = () => {
    setLoading(true);
    fetchReviews()
      .then((data) => {
        const approvedReviews = Array.isArray(data)
          ? data.filter((review) => review.is_approved)
          : [];
        setReviews(approvedReviews);
        setLoading(false);
      })
      .catch(() => {
        setReviews([]);
        setLoading(false);
      });
  };

  const handleReviewSuccess = () => {
    refreshReviews();
    setShowSuccess(true);
  };

  useEffect(() => {
    refreshReviews();
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
      aria-label="Vélemények oldal"
      tabIndex={0}
    >
      {/* Háttérkép */}
      <img
        src="/reviewpage.webp"
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
      {/* Cím a tetején */}
      <Box
        sx={{
          position: "relative",
          zIndex: 2,
          backgroundColor:
            mode === "dark" ? "rgba(30,30,30,0.92)" : "rgba(255,255,255,0.85)",
          borderRadius: 4,
          p: { xs: 2, sm: 4 },
          boxShadow: "md",
          maxWidth: 420,
          width: { xs: "95%", sm: "80%", md: "420px" },
          textAlign: "center",
          mt: { xs: 4, sm: 6 },
          opacity: 0,
          transform: "translateY(32px)",
          animation: "fadeInUp 0.8s cubic-bezier(.4,0,.2,1) 0.1s forwards",
        }}
      >
        <Typography
          level="h1"
          sx={{
            mb: 2,
            fontSize: { xs: "2rem", sm: "2.5rem" },
            color: mode === "dark" ? "#fff" : "#121212",
            fontWeight: 700,
            letterSpacing: "0.02em",
            textAlign: "center",
            opacity: 0,
            animation: "fadeInUp 0.8s cubic-bezier(.4,0,.2,1) 0.2s forwards",
          }}
          tabIndex={0}
        >
          Vélemények
        </Typography>
      </Box>
      {/* Körhinta animáltan, késleltetve */}
      <Box
        sx={{
          position: "relative",
          zIndex: 2,
          width: "100%",
          maxWidth: 420,
          mt: 3,
          opacity: 0,
          transform: "translateY(32px)",
          animation: "fadeInUp 0.8s cubic-bezier(.4,0,.2,1) 0.6s forwards",
        }}
      >
        {loading ? <ReviewsSkeleton /> : <ReviewsCarousel reviews={reviews} />}
      </Box>
      {/* Vélemény beküldő gomb legalul, utolsóként animálva */}
      <Box
        sx={{
          position: "relative",
          zIndex: 2,
          width: "100%",
          maxWidth: 420,
          mt: 4,
          mb: 2,
          opacity: 0,
          transform: "translateY(32px)",
          animation: "fadeInUp 0.8s cubic-bezier(.4,0,.2,1) 1.1s forwards",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {/* Pulzáló kék effekt a gomb körül */}
        <span
          aria-hidden="true"
          style={{
            position: "absolute",
            left: 0,
            top: 0,
            width: "100%",
            height: "100%",
            borderRadius: 4,
            background: "linear-gradient(90deg, #90caf9 0%, transparent 100%)",
            opacity: 0.25,
            zIndex: 0,
            pointerEvents: "none",
            animation: "rectPulse 2.5s infinite cubic-bezier(.4,0,.2,1)",
          }}
        />
        <CreateReviewButton onSuccess={handleReviewSuccess} />
        <style>
          {`
            @keyframes rectPulse {
              0% {
                opacity: 0.25;
                transform: scale(0.98);
              }
              50% {
                opacity: 0.4;
                transform: scale(1.08);
              }
              100% {
                opacity: 0.25;
                transform: scale(0.98);
              }
            }
          `}
        </style>
      </Box>
      {/* Sikeres mentés visszajelzés */}
      <SuccessSnackbar
        open={showSuccess}
        onClose={() => setShowSuccess(false)}
      />
      {/* Animációs kulcsszavak */}
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
        `}
      </style>
    </Box>
  );
}

export default ReviewsPage;
