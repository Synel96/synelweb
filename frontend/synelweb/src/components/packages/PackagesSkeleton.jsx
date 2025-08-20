import { Box, Skeleton } from "@mui/joy";

function PackagesSkeleton({ count = 3 }) {
  return (
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
        mt: 2,
      }}
      aria-hidden="true"
    >
      {Array.from({ length: count }).map((_, idx) => (
        <Box
          key={idx}
          sx={{
            flex: "1 1 320px",
            maxWidth: 340,
            minWidth: 260,
            bgcolor: "background.level1",
            borderRadius: 4,
            boxShadow: "md",
            p: { xs: 2, sm: 3 },
            mb: 2,
            display: "flex",
            flexDirection: "column",
            gap: 2,
            position: "relative",
          }}
        >
          <Skeleton
            variant="rectangular"
            width="80%"
            height={32}
            sx={{ mb: 1, borderRadius: 2 }}
          />
          <Skeleton variant="text" width="95%" sx={{ mb: 1 }} />
          <Skeleton variant="text" width="90%" sx={{ mb: 1 }} />
          <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap", mb: 1 }}>
            <Skeleton variant="rounded" width={60} height={24} />
            <Skeleton variant="rounded" width={48} height={24} />
            <Skeleton variant="rounded" width={40} height={24} />
          </Box>
        </Box>
      ))}
    </Box>
  );
}
export default PackagesSkeleton;
