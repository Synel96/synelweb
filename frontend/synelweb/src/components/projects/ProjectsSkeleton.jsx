import { Box, Skeleton } from "@mui/joy";

function ProjectsSkeleton() {
  return (
    <Box
      role="region"
      aria-label="Projektek betöltése folyamatban"
      sx={{
        display: "flex",
        flexDirection: { xs: "column", sm: "row" },
        gap: 3,
        width: "100%",
        justifyContent: { xs: "center", sm: "flex-start" },
        alignItems: { xs: "stretch", sm: "flex-start" },
        py: 2,
      }}
      tabIndex={0}
    >
      {[1, 2, 3].map((item) => (
        <Box
          key={item}
          sx={{
            flex: "1 1 280px",
            minWidth: { xs: "90%", sm: 280 },
            maxWidth: 340,
            bgcolor: "background.level1",
            borderRadius: 3,
            boxShadow: "md",
            p: 2,
            display: "flex",
            flexDirection: "column",
            gap: 2,
            mb: { xs: 3, sm: 0 },
          }}
          aria-label={`Projekt kártya skeleton ${item}`}
          tabIndex={0}
        >
          <Skeleton
            variant="rectangular"
            height={160}
            sx={{ borderRadius: 2 }}
          />
          <Skeleton variant="text" width="60%" height={32} />
          <Skeleton variant="text" width="80%" height={24} />
          <Skeleton variant="text" width="40%" height={24} />
        </Box>
      ))}
    </Box>
  );
}

export default ProjectsSkeleton;
