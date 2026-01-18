import { Box, Typography, Chip, Button } from "@mui/joy";
import { useState, useRef, useLayoutEffect } from "react";
import PercentIcon from "@mui/icons-material/Percent";

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
      sx={{
        width: "100%",
        maxWidth: { xs: "100%", sm: 520 },
        bgcolor: "background.surface",
        borderRadius: 4,
        boxShadow: "lg",
        border: "2px solid",
        borderColor: "divider",
        p: { xs: 2, sm: 3 },
        mb: 4,
        display: "flex",
        flexDirection: "column",
        gap: 2,
        position: "relative",
        cursor: "pointer",
        transition: "box-shadow 0.3s, border-color 0.3s",
        "&:active": {
          boxShadow: "0 0 24px rgba(255,140,0,0.6)",
          borderColor: "rgba(255,140,0,0.8)",
        },
        ...sx,
      }}
      role="region"
      aria-label={`Csomag: ${name}`}
      tabIndex={0}
    >
      {/* % ikon */}
      {is_discounted && (
        <Box
          sx={{
            position: "absolute",
            top: 8,
            right: 12,
            zIndex: 3,
            background: "#ff9800",
            color: "#fff",
            borderRadius: "50%",
            width: 36,
            height: 36,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: "0 2px 8px rgba(0,0,0,0.10)",
          }}
          aria-label="Akciós csomag"
        >
          <PercentIcon fontSize="small" sx={{ color: "#ff1744" }} />
        </Box>
      )}

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
              aria-label={`Eredeti ár: ${parseInt(price, 10)} Ft`}
              tabIndex={0}
            >
              {parseInt(price, 10)} Ft
            </Typography>
            <Typography
              sx={{
                color: "#39ff14",
                fontWeight: 700,
                fontSize: "1.25rem",
                display: "inline",
              }}
              aria-label={`Akciós ár: ${parseInt(discounted_price, 10)} Ft`}
              tabIndex={0}
            >
              {parseInt(discounted_price, 10)} Ft
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
              aria-label={`Ár: ${parseInt(price, 10)} Ft`}
              tabIndex={0}
            >
              {parseInt(price, 10)} Ft
            </Typography>
          )
        )}
      </Box>
    </Box>
  );
}

export default PackagesCards;
