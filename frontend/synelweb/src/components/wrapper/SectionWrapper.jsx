import { useRef, useEffect, useState } from "react";

function SectionWrapper({ id, children, delay = 0 }) {
  const ref = useRef();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const observer = new window.IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setTimeout(() => setVisible(true), delay);
        }
      },
      { threshold: 0.2 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [delay]);

  return (
    <section
      id={id}
      ref={ref}
      className={`fade-in${visible ? " visible" : ""}`}
      style={{ 
        width: "100%", 
        paddingTop: "2rem", 
        paddingBottom: "2rem",
        contentVisibility: "auto",
        containIntrinsicSize: "auto 500px"
      }}
    >
      {children}
    </section>
  );
}

export default SectionWrapper;
