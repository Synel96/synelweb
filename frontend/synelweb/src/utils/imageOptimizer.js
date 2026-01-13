/**
 * Cloudinary image optimizer utility
 * Provides optimized image URLs with automatic format conversion and responsive sizing
 */

const CLOUDINARY_CLOUD_NAME = 'dmwulp3dl'; // Your Cloudinary cloud name
const CLOUDINARY_BASE_URL = `https://res.cloudinary.com/${CLOUDINARY_CLOUD_NAME}/image/upload`;

/**
 * Generate optimized Cloudinary URL with transformations
 * @param {string} publicId - Cloudinary public ID (e.g., 'backgrounds/hero')
 * @param {object} options - Transformation options
 * @returns {string} - Optimized Cloudinary URL
 */
export function getCloudinaryUrl(publicId, options = {}) {
  const {
    width = 'auto',
    quality = 'auto:good',
    format = 'auto',
    crop = 'fill',
    dpr = 'auto',
    fetchFormat = 'auto',
  } = options;

  const transformations = [
    `w_${width}`,
    `q_${quality}`,
    `f_${format}`,
    `c_${crop}`,
    `dpr_${dpr}`,
    'fl_progressive',
    'fl_lossy',
  ].join(',');

  return `${CLOUDINARY_BASE_URL}/${transformations}/${publicId}`;
}

/**
 * Generate responsive srcset for background images
 * @param {string} publicId - Cloudinary public ID
 * @returns {string} - srcset attribute value
 */
export function getResponsiveSrcSet(publicId) {
  const widths = [640, 768, 1024, 1280, 1536, 1920];
  return widths
    .map((w) => `${getCloudinaryUrl(publicId, { width: w, quality: 'auto:good' })} ${w}w`)
    .join(', ');
}

/**
 * Generate optimized logo URL
 * @param {string} publicId - Cloudinary public ID
 * @param {number} size - Logo size in pixels
 * @returns {string} - Optimized logo URL
 */
export function getOptimizedLogo(publicId, size = 120) {
  return getCloudinaryUrl(publicId, {
    width: size * 2, // 2x for retina
    quality: 'auto:best',
    crop: 'scale',
  });
}

/**
 * Preload critical images
 * @param {string} src - Image source URL
 * @param {string} type - Image type (default: 'image/webp')
 */
export function preloadImage(src, type = 'image/webp') {
  const link = document.createElement('link');
  link.rel = 'preload';
  link.as = 'image';
  link.href = src;
  link.type = type;
  document.head.appendChild(link);
}

/**
 * Background image URLs mapping
 * Upload these images to Cloudinary and update the public IDs
 */
export const BACKGROUND_IMAGES = {
  hero: 'synelweb/backgrounds/hero',
  contact: 'synelweb/backgrounds/contact',
  contactPage: 'synelweb/backgrounds/contactpage',
  packages: 'synelweb/backgrounds/packages',
  packagesPage: 'synelweb/backgrounds/packagespage',
  projects: 'synelweb/backgrounds/projects',
  projectsPage: 'synelweb/backgrounds/projectspage',
  review: 'synelweb/backgrounds/review',
  reviewPage: 'synelweb/backgrounds/reviewpage',
};

/**
 * Logo URLs mapping
 */
export const LOGOS = {
  dark: 'synelweb/logos/darklogo',
  light: 'synelweb/logos/lightlogo',
  main: 'synelweb/logos/logo',
};
