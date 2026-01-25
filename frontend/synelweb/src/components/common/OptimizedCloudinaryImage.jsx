import { useState } from "react";
import { Box } from "@mui/joy";

/**
 * Optimalized Cloudinary image component for project images with responsive optimization
 * @param {string} cloudinaryId - Cloudinary public_id (e.g., "projects/image_abc123")
 * @param {string} alt - Alt text for accessibility
 * @param {string} aspectRatio - CSS aspect ratio (default: "16/9")
 * @param {boolean} priority - If true, loads eagerly with high priority for LCP optimization
 * @param {object} sx - Additional MUI sx props
 */
function OptimizedCloudinaryImage({ 
  cloudinaryId, 
  alt = "", 
  aspectRatio = "16/9",
  priority = false,
  sx = {} 
}) {
  const [loaded, setLoaded] = useState(false);
  const CLOUDINARY_BASE = 'https://res.cloudinary.com/dmwulp3dl/image/upload';

  // Generate responsive srcset with optimizations
  const generateUrl = (width, quality = 75) => {
    // Transformations: width, quality, format auto, progressive, compression
    return `${CLOUDINARY_BASE}/w_${width},q_${quality},f_auto,fl_progressive,c_limit/${cloudinaryId}`;
  };

  const srcSet = [
    `${generateUrl(400)} 400w`,
    `${generateUrl(640)} 640w`,
    `${generateUrl(768)} 768w`,
    `${generateUrl(1024)} 1024w`,
    `${generateUrl(1280)} 1280w`,
    `${generateUrl(1536)} 1536w`,
  ].join(', ');

  const sizes = "(max-width: 640px) 400px, (max-width: 768px) 640px, (max-width: 1024px) 768px, 1024px";

  if (!cloudinaryId) {
    return (
      <Box
        sx={{
          width: "100%",
          aspectRatio,
          bgcolor: "background.level2",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          borderRadius: 2,
          ...sx
        }}
      >
        Nincs elérhető kép
      </Box>
    );
  }

  return (
    <Box
      suppressHydrationWarning
      sx={{
        position: "relative",
        width: "100%",
        aspectRatio,
        overflow: "hidden",
        bgcolor: "background.level2",
        ...sx
      }}
    >
      {/* Loading placeholder */}
      {!loaded && (
        <Box
          sx={{
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            bgcolor: "background.level2",
            animation: "pulse 1.5s ease-in-out infinite",
            "@keyframes pulse": {
              "0%, 100%": { opacity: 1 },
              "50%": { opacity: 0.5 }
            }
          }}
        />
      )}
      
      {/* Optimized image */}
      <img
        src={generateUrl(768)} // Default size for src
        srcSet={srcSet}
        sizes={sizes}
        alt={alt}
        loading={priority ? "eager" : "lazy"}
        fetchPriority={priority ? "high" : "auto"}
        decoding={priority ? "sync" : "async"}
        onLoad={() => setLoaded(true)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          opacity: loaded ? 1 : 0,
          transition: "opacity 0.3s ease-in-out"
        }}
      />
    </Box>
  );
}

export default OptimizedCloudinaryImage;
