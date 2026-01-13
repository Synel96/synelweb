/**
 * Optimized background image component with responsive srcset
 * Generates multiple image sizes for different viewports
 */
function OptimizedBackgroundImage({ 
  src, 
  alt, 
  loading = 'lazy',
  priority = false,
  style = {},
  ...props 
}) {
  // Extract base path without query params
  const baseSrc = src.split('?')[0];
  
  // Generate srcset for responsive images
  const srcSet = [
    `${baseSrc}?w=640&format=webp&q=75 640w`,
    `${baseSrc}?w=768&format=webp&q=75 768w`,
    `${baseSrc}?w=1024&format=webp&q=75 1024w`,
    `${baseSrc}?w=1280&format=webp&q=75 1280w`,
    `${baseSrc}?w=1536&format=webp&q=75 1536w`,
    `${baseSrc}?w=1920&format=webp&q=75 1920w`,
  ].join(', ');

  // Default fallback (1920px WebP)
  const defaultSrc = `${baseSrc}?w=1920&format=webp&q=75`;

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
          imagesrcset={srcSet}
          imagesizes="100vw"
        />
      )}
      <img
        src={defaultSrc}
        srcSet={srcSet}
        sizes="100vw"
        alt={alt}
        loading={priority ? 'eager' : loading}
        fetchpriority={priority ? 'high' : 'auto'}
        decoding={priority ? 'sync' : 'async'}
        style={defaultStyle}
        aria-hidden="true"
        {...props}
      />
    </>
  );
}

export default OptimizedBackgroundImage;
