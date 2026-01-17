import { Box, Typography, Chip, Button } from "@mui/joy";
import { useState, useRef, useLayoutEffect } from "react";

function PackagesCards({
  name,
  description,
  tags = [],
  is_discounted,
  preview_image_url,
  price,
  discounted_price,
  sx = {},
}) {
  const [expanded, setExpanded] = useState(false);
  const [isActive, setIsActive] = useState(false);
  const descRef = useRef(null);
  const [descHeight, setDescHeight] = useState("auto");

  useLayoutEffect(() => {
    if (descRef.current && expanded) {
      setDescHeight(descRef.current.scrollHeight + "px");
    } else {
      setDescHeight("60px"); // kb. 3 sor magasság
    }
  }, [expanded, description]);

  return (
    <Box
      onClick={() => setIsActive(!isActive)}
      onTouchStart={() => setIsActive(!isActive)}
      sx={{
        bgcolor: "background.surface",
        borderRadius: 4,
        border: "2px solid",
        borderColor: isActive 
          ? (is_discounted ? "rgba(255,152,0,0.8)" : "rgba(255,140,0,0.5)")
          : (is_discounted ? "rgba(255,152,0,0.6)" : "divider"),
        boxShadow: isActive
          ? (is_discounted
            ? "0 0 40px 16px rgba(255,152,0,0.5), 0 0 32px 8px rgba(255,140,0,0.3)"
            : "xl")
          : (is_discounted
            ? "0 0 32px 12px rgba(255,152,0,0.3)"
            : "lg"),
        p: { xs: 2, sm: 3 },
        display: "flex",
        flexDirection: "column",
        gap: 2,
        position: "relative",
        transition: "box-shadow 0.3s, filter 0.3s, transform 0.3s, border-color 0.3s",
        animation: is_discounted
          ? "discountPulse 1.8s infinite cubic-bezier(.4,0,.2,1)"
          : undefined,
        filter: isActive ? "brightness(0.98)" : "brightness(1)",
        transform: isActive
          ? (is_discounted
            ? "translateY(-5px) scale(1.02)"
            : "translateY(-8px) scale(1.03)")
          : "translateY(0) scale(1)",
        cursor: "pointer",
        ...sx,
      }}
      role="article"
      aria-label={`Csomag: ${name}`}
      tabIndex={0}
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
      <Box
        sx={{
          overflow: "hidden",
          transition: "height 0.35s cubic-bezier(.4,0,.2,1), opacity 0.3s",
          height: descHeight,
          opacity: expanded ? 1 : 0.95,
          mb: 1,
        }}
      >
        <Typography
          ref={descRef}
          level="body2"
          sx={{
            color: "text.secondary",
            textAlign: "left",
            display: "-webkit-box",
            WebkitLineClamp: expanded ? "unset" : 3,
            WebkitBoxOrient: "vertical",
            overflow: expanded ? "visible" : "hidden",
            textOverflow: expanded ? "unset" : "ellipsis",
            transition: "all 0.2s",
          }}
          aria-label={`Csomag leírása: ${description}`}
          tabIndex={0}
        >
          {description}
        </Typography>
      </Box>
      {!expanded && (
        <Button
          size="sm"
          variant="soft"
          sx={{ alignSelf: "flex-start", mt: -1, mb: 1 }}
          onClick={() => setExpanded(true)}
        >
          Mutasd az összeset
        </Button>
      )}
      {expanded && (
        <Button
          size="sm"
          variant="soft"
          sx={{ alignSelf: "flex-start", mt: -1, mb: 1 }}
          onClick={() => setExpanded(false)}
        >
          Bezárás
        </Button>
      )}
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
      {/* Pulzáló animáció stílus */}
      <style>
        {`
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
