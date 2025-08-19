function Logo({ src, isMobile }) {
  return (
    <img
      src={src}
      alt="Synel Web Solutions logó"
      style={{
        width: 120,
        margin: isMobile ? "0 auto" : "0",
        position: "static",
        zIndex: 2,
        display: "block",
        transition: "transform 0.2s, filter 0.2s",
        cursor: "pointer",
        outline: "none",
      }}
      tabIndex={0}
      aria-label="Synel Web Solutions logó"
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "scale(1.08)";
        e.currentTarget.style.filter = "drop-shadow(0 0 8px #1976d2)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "scale(1)";
        e.currentTarget.style.filter = "none";
      }}
      onTouchStart={(e) => {
        e.currentTarget.style.transform = "scale(1.08)";
        e.currentTarget.style.filter = "drop-shadow(0 0 8px #1976d2)";
      }}
      onTouchEnd={(e) => {
        e.currentTarget.style.transform = "scale(1)";
        e.currentTarget.style.filter = "none";
      }}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.currentTarget.style.transform = "scale(1.08)";
          e.currentTarget.style.filter = "drop-shadow(0 0 8px #1976d2)";
        }
      }}
      onKeyUp={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.currentTarget.style.transform = "scale(1)";
          e.currentTarget.style.filter = "none";
        }
      }}
    />
  );
}

export default Logo;
