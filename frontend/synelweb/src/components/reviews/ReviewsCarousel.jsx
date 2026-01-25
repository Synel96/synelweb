import { useEffect, useState, useRef } from "react";
import {
  Box,
  Typography,
  Card,
  CardContent,
  Stack,
  IconButton,
} from "@mui/joy";
import StarIcon from "@mui/icons-material/Star";
import ArrowBackIosNewIcon from "@mui/icons-material/ArrowBackIosNew";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";

function ReviewsCarousel({ reviews = [] }) {
  const [current, setCurrent] = useState(0);
  const timerRef = useRef();

  useEffect(() => {
    if (reviews.length > 0) {
      timerRef.current = setInterval(() => {
        setCurrent((prev) => (prev + 1) % reviews.length);
      }, 5000);
      return () => clearInterval(timerRef.current);
    }
  }, [reviews.length]);

  const handlePrev = () =>
    setCurrent((prev) => (prev === 0 ? reviews.length - 1 : prev - 1));
  const handleNext = () => setCurrent((prev) => (prev + 1) % reviews.length);

  if (!Array.isArray(reviews) || reviews.length === 0) {
    return (
      <Box
        sx={{
          width: "100%",
          maxWidth: 420,
          mx: "auto",
          mt: { xs: 2, sm: 4 },
          mb: { xs: 2, sm: 4 },
          position: "relative",
          outline: "none",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: 180,
          backgroundColor: "background.surface",
          borderRadius: 4,
          boxShadow: "md",
        }}
        role="region"
        aria-label="Vélemények karusszel"
        tabIndex={0}
      >
        <Typography
          level="body2"
          sx={{ color: "text.secondary", textAlign: "center" }}
        >
          Oszd meg a véleményed — számít a visszajelzésed!
        </Typography>
      </Box>
    );
  }

  // Biztonságos review lekérés
  const review = reviews[current] || {};
  const rating = Number(review.rating) > 0 ? Number(review.rating) : 0;
  const dateStr =
    review.created_at && !isNaN(Date.parse(review.created_at))
      ? new Date(review.created_at).toLocaleDateString("hu-HU")
      : "";

  return (
    <Box
      suppressHydrationWarning
      sx={{
        width: "100%",
        maxWidth: 420,
        mx: "auto",
        mt: { xs: 2, sm: 4 },
        mb: { xs: 2, sm: 4 },
        position: "relative",
        outline: "none",
      }}
      role="region"
      aria-label="Vélemények karusszel"
      tabIndex={0}
    >
      <Card
        variant="soft"
        sx={{
          p: { xs: 2, sm: 3 },
          borderRadius: 4,
          boxShadow: "md",
          backgroundColor: "background.surface",
          minHeight: 180,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          transition: "box-shadow 0.3s, border-color 0.3s",
          "&:hover": {
            boxShadow:
              "0 0 32px 8px rgba(30, 136, 229, 0.25), 0 2px 8px rgba(0,0,0,0.10)",
            borderColor: "#1976d2",
          },
          border: "2px solid transparent",
        }}
      >
        <CardContent sx={{ width: "100%" }}>
          <Stack
            direction="row"
            spacing={1}
            alignItems="center"
            justifyContent="center"
            sx={{ mb: 1 }}
          >
            {[...Array(rating)].map((_, i) => (
              <StarIcon
                key={i}
                sx={{ color: "#FFD700" }}
                aria-label="Csillag"
              />
            ))}
          </Stack>
          <Typography
            level="body1"
            sx={{
              fontSize: { xs: "1rem", sm: "1.1rem" },
              color: "text.primary",
              textAlign: "center",
              mb: 2,
            }}
            tabIndex={0}
          >
            {review.comment || ""}
          </Typography>
          <Typography
            level="body2"
            sx={{
              color: "text.secondary",
              textAlign: "center",
              fontStyle: "italic",
            }}
            tabIndex={0}
          >
            {review.name || ""}
          </Typography>
          <Typography
            level="body3"
            sx={{
              color: "text.tertiary",
              textAlign: "center",
              fontSize: "0.85rem",
              mt: 1,
            }}
            tabIndex={0}
          >
            {dateStr}
          </Typography>
        </CardContent>
      </Card>
      <IconButton
        aria-label="Előző vélemény"
        onClick={handlePrev}
        sx={{
          position: "absolute",
          left: 8,
          top: "50%",
          transform: "translateY(-50%)",
          zIndex: 3,
          bgcolor: "background.level1",
          "&:focus": { outline: "2px solid #1976d2" },
        }}
        tabIndex={0}
      >
        <ArrowBackIosNewIcon />
      </IconButton>
      <IconButton
        aria-label="Következő vélemény"
        onClick={handleNext}
        sx={{
          position: "absolute",
          right: 8,
          top: "50%",
          transform: "translateY(-50%)",
          zIndex: 3,
          bgcolor: "background.level1",
          "&:focus": { outline: "2px solid #1976d2" },
        }}
        tabIndex={0}
      >
        <ArrowForwardIosIcon />
      </IconButton>
      <Box sx={{ textAlign: "center", mt: 1 }}>
        <Typography level="body3" sx={{ color: "text.tertiary" }}>
          {current + 1} / {reviews.length}
        </Typography>
      </Box>
    </Box>
  );
}

export default ReviewsCarousel;
