import { Box, Typography, Chip } from "@mui/joy";

function PackagesCards({
  name,
  description,
  tags = [],
  is_discounted,
  preview_image_url,
  price,
  discounted_price,
}) {
  return (
    <Box
      sx={{
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
      role="article"
      aria-label={`Csomag: ${name}`}
    >
      {/* Előnézeti kép */}
      {preview_image_url && (
        <Box
          sx={{
            width: "100%",
            height: 120,
            mb: 1,
            borderRadius: 3,
            overflow: "hidden",
            background: "#f5f5f5",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <img
            src={preview_image_url}
            alt={`${name} előnézeti kép`}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              borderRadius: "8px",
            }}
          />
        </Box>
      )}
      {/* Név */}
      <Typography
        level="h2"
        sx={{
          fontSize: { xs: "1.2rem", sm: "1.5rem" },
          fontWeight: 700,
          color: "text.primary",
          mb: 1,
          textAlign: "left",
        }}
        aria-label={`Csomag neve: ${name}`}
        tabIndex={0}
      >
        {name}
      </Typography>
      {/* Leírás */}
      <Typography
        level="body2"
        sx={{
          color: "text.secondary",
          mb: 1,
          textAlign: "left",
        }}
        aria-label={`Csomag leírása: ${description}`}
        tabIndex={0}
      >
        {description}
      </Typography>
      {/* Címkék */}
      {tags && tags.length > 0 && (
        <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap", mb: 1 }}>
          {tags.map((tag, idx) => (
            <Chip
              key={idx}
              color="primary"
              variant="soft"
              sx={{ fontSize: "0.95rem" }}
              aria-label={`Címke: ${tag}`}
              tabIndex={0}
            >
              {tag}
            </Chip>
          ))}
        </Box>
      )}
      {/* Ár megjelenítése */}
      <Box sx={{ mt: 2, textAlign: "left" }}>
        {is_discounted && discounted_price ? (
          <>
            <Typography
              sx={{
                textDecoration: "line-through",
                color: "text.secondary",
                fontSize: "1.1rem",
                mr: 1,
                display: "inline",
              }}
              aria-label={`Eredeti ár: ${price} Ft`}
              tabIndex={0}
            >
              {price} Ft
            </Typography>
            <Typography
              sx={{
                color: "#39ff14", // neon zöld mindkét módban
                fontWeight: 700,
                fontSize: "1.25rem",
                display: "inline",
              }}
              aria-label={`Akciós ár: ${discounted_price} Ft`}
              tabIndex={0}
            >
              {discounted_price} Ft
            </Typography>
          </>
        ) : (
          price && (
            <Typography
              sx={{
                color: "text.primary",
                fontWeight: 700,
                fontSize: "1.15rem",
              }}
              aria-label={`Ár: ${price} Ft`}
              tabIndex={0}
            >
              {price} Ft
            </Typography>
          )
        )}
      </Box>
    </Box>
  );
}

export default PackagesCards;

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
    alignItems: "flex-start", // vagy töröld ezt a sort
    alignContent: "flex-start",
  }}
  role="region"
  aria-label="Szolgáltatáscsomagok listája"
>
  {/* ...kártyák... */}
</Box>;
