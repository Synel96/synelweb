function Logo({ src, isMobile }) {
  return (
    <img
      src={src}
      alt="Synel Web Solutions logó"
      width="180"
      height="60"
      fetchpriority="high"
      style={{
        width: 180,
        height: 60,
        objectFit: "contain",
        margin: isMobile ? "0 auto" : "0",
        position: "static",
        zIndex: 2,
        display: "block",
        transition: "transform 0.2s",
        cursor: "pointer",
        outline: "none",
        willChange: "transform",
      }}
      tabIndex={0}
      aria-label="Synel Web Solutions logó"
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "scale(1.05)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "scale(1)";
      }}
      onTouchStart={(e) => {
        e.currentTarget.style.transform = "scale(1.05)";
      }}
      onTouchEnd={(e) => {
        e.currentTarget.style.transform = "scale(1)";
      }}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.currentTarget.style.transform = "scale(1.05)";
        }
      }}
      onKeyUp={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.currentTarget.style.transform = "scale(1)";
        }
      }}
    />
  );
}

export default Logo;
