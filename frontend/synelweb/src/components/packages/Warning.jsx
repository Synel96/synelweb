import { Box, Typography } from "@mui/joy";

function Warning() {
  return (
    <Box
      sx={{
        background: "#fff3e0",
        border: "1px solid #ff9800",
        borderRadius: 3,
        p: 2,
        mb: 3,
        display: "flex",
        alignItems: "center",
        gap: 2,
      }}
      role="alert"
      aria-label="Árfigyelmeztetés"
    >
      <Typography level="body2" sx={{ color: "#d84315", fontWeight: 600 }}>
        Az oldalon feltüntetett árak tájékoztató jellegűek, nem minősülnek
        végleges ajánlatnak. A fejlesztés pontos költsége minden esetben az
        ügyféllel közösen, a specifikáció egyeztetése után kerül meghatározásra.
        Az árat jelentősen befolyásolja a kért funkciók komplexitása és
        megvalósításának nehézsége, így a végső összeg akár lényegesen kevesebb
        vagy több is lehet.
      </Typography>
    </Box>
  );
}

export default Warning;
