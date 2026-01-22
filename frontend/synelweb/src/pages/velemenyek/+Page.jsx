import { useColorScheme } from "@mui/joy/styles";
import Sheet from "@mui/joy/Sheet";
import Box from "@mui/joy/Box";
import Typography from "@mui/joy/Typography";
import ReviewsCarousel from "../../components/reviews/ReviewsCarousel";
import CreateReviewButton from "../../components/reviews/CreateReviewButton";
import { useEffect, useState } from "react";
import { fetchReviews } from "../../services/reviewsService";
import SuccessSnackbar from "../../components/modals/SucessSnackbar";
import ReviewsSkeleton from "../../components/reviews/ReviewsSkeleton";
import OptimizedBackgroundImage from "../../components/common/OptimizedBackgroundImage";

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
    <Sheet
      component="section"
      sx={{
        position: "relative",
        width: "100vw",
        minHeight: { xs: "60vw", sm: "60vw", md: "60vw" },
        maxHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        overflow: "hidden",
        p: 0,
        m: 0,
        transition: "background 0.3s",
      }}
      variant="plain"
      role="region"
      aria-label="Vélemények szekció"
      tabIndex={0}
    >
      {/* Cloudinary optimalizált háttérkép */}
      <OptimizedBackgroundImage 
        cloudinaryId="reviewpage_ub16ki"
        alt="Vélemények háttérkép"
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
          width: { xs: "95%", sm: "80%", md: "420px" },
          mx: "auto",
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
          mx: "auto",
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
          mx: "auto",
          opacity: 0,
          transform: "translateY(32px)",
          animation: "fadeInUp 0.8s cubic-bezier(.4,0,.2,1) 1.1s forwards",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <CreateReviewButton onSuccess={handleReviewSuccess} />
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
    </Sheet>
  );
}

export default ReviewsPage;
