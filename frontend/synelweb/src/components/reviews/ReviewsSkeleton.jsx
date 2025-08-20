import { Box, Skeleton, Stack } from "@mui/joy";

function ReviewsSkeleton() {
  return (
    <Box
      sx={{
        width: "100%",
        maxWidth: 420,
        mx: "auto",
        p: { xs: 2, sm: 4 },
        borderRadius: 4,
        boxShadow: "md",
        backgroundColor: "background.surface",
      }}
      aria-label="Vélemények betöltése folyamatban"
      role="status"
    >
      <Stack spacing={2}>
        {/* Név */}
        <Skeleton variant="text" width="60%" height={28} sx={{ mx: "auto" }} />
        {/* Értékelés csillagok helye */}
        <Skeleton
          variant="rectangular"
          width={120}
          height={28}
          sx={{ mx: "auto", borderRadius: 2 }}
        />
        {/* Vélemény szöveg */}
        <Skeleton variant="text" width="90%" height={22} sx={{ mx: "auto" }} />
        <Skeleton variant="text" width="80%" height={22} sx={{ mx: "auto" }} />
        {/* Dátum */}
        <Skeleton variant="text" width="40%" height={18} sx={{ mx: "auto" }} />
      </Stack>
    </Box>
  );
}

export default ReviewsSkeleton;
