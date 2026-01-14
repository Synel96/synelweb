/**
 * Optimized background image component with Cloudinary
 * Automatically optimizes images with responsive sizes and modern formats
 */
function OptimizedBackgroundImage({ 
  cloudinaryId,
  alt, 
  loading = 'lazy',
  priority = false,
  style = {},
  ...props 
}) {
  const CLOUDINARY_BASE = 'https://res.cloudinary.com/dmwulp3dl/image/upload';
  
  // Generate Cloudinary transformations for different sizes
  const generateUrl = (width, quality = 75) => {
    return `${CLOUDINARY_BASE}/w_${width},q_${quality},f_auto,fl_progressive/${cloudinaryId}`;
  };
  
  // Generate srcset for responsive images
  const srcSet = [
    `${generateUrl(640)} 640w`,
    `${generateUrl(768)} 768w`,
    `${generateUrl(1024)} 1024w`,
    `${generateUrl(1280)} 1280w`,
    `${generateUrl(1536)} 1536w`,
    `${generateUrl(1920)} 1920w`,
  ].join(', ');

  // Default fallback (1920px)
  const defaultSrc = generateUrl(1920);

  const defaultStyle = {
    position: 'absolute',
    inset: 0,
    width: '100vw',
    height: '100%',
    objectFit: 'cover',
    zIndex: 1,
    pointerEvents: 'none',
    ...style,
  };

  return (
    <>
      {/* Preload hint for LCP images */}
      {priority && (
        <link
          rel="preload"
          as="image"
          href={defaultSrc}
          imageSrcSet={srcSet}
          imageSizes="100vw"
        />
      )}
      <img
        src={defaultSrc}
        srcSet={srcSet}
        sizes="100vw"
        alt={alt}
        loading={priority ? 'eager' : loading}
        fetchPriority={priority ? 'high' : 'auto'}
        decoding={priority ? 'sync' : 'async'}
        style={defaultStyle}
        aria-hidden="true"
        {...props}
      />
    </>
  );
}

export default OptimizedBackgroundImage;
