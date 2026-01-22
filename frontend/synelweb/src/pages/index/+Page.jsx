import { useState } from "react";
import HeroSection from "../../components/hero/HeroSection";
import ContactSection from "../../components/contactsection/ContactSection";
import ReviewSection from "../../components/reviewsection/ReviewSection";
import ProjectsSection from "../../components/projectssection/ProjectsSection";
import PackagesSection from "../../components/packagessection/PackagesSection";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward";
import SectionWrapper from "../../components/wrapper/SectionWrapper";
import "../../App.css";

const sectionIds = [
  "section-1",
  "section-2",
  "section-3",
  "section-4",
  "section-5",
];

function MainPage() {
  const scrollToNextSection = () => {
    const sections = sectionIds.map((id) => document.getElementById(id));
    const scrollY = window.scrollY;
    const nextIndex = sections.findIndex(
      (section) =>
        section && section.getBoundingClientRect().top + scrollY > scrollY + 10
    );
    const targetSection = sections[nextIndex !== -1 ? nextIndex : 1];
    if (targetSection) {
      targetSection.scrollIntoView({ behavior: "smooth" });
    }
  };

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <main>
      <SectionWrapper id="section-1">
        <HeroSection />
      </SectionWrapper>
      {/* Le nyíl - csak mobil/tablet, jobb oldalon */}
      <ArrowDownwardIcon
        sx={{
          display: "inline-flex",
          position: "fixed",
          right: { xs: 16, sm: 24 },
          bottom: { xs: 20, sm: 24 },
          zIndex: 100,
          fontSize: { xs: 36, sm: 38 },
          color: "#ff9800",
          cursor: "pointer",
          animation: "bounce 1.2s infinite",
          background: "rgba(255,255,255,0.85)",
          borderRadius: "50%",
          boxShadow: "0 2px 8px rgba(0,0,0,0.10)",
          p: 0.5,
        }}
        onClick={scrollToNextSection}
      />
      {/* Fel nyíl - mindig látszik, jobb oldalon, kicsit feljebb, animált */}
      <ArrowUpwardIcon
        sx={{
          position: "fixed",
          right: { xs: 16, sm: 24 },
          bottom: { xs: 72, sm: 80 },
          zIndex: 100,
          fontSize: { xs: 36, sm: 38 },
          color: "#ff9800",
          cursor: "pointer",
          background: "rgba(255,255,255,0.85)",
          borderRadius: "50%",
          boxShadow: "0 2px 8px rgba(0,0,0,0.10)",
          p: 0.5,
          display: "inline-flex",
          animation: "bounceUp 1.2s infinite",
        }}
        onClick={scrollToTop}
      />
      <style>
        {`
          @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(14px); }
          }
          @keyframes bounceUp {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-14px); }
          }
        `}
      </style>
      <SectionWrapper id="section-2" delay={0}>
        <ContactSection />
      </SectionWrapper>
      <SectionWrapper id="section-3" delay={400}>
        <ProjectsSection />
      </SectionWrapper>
      <SectionWrapper id="section-4" delay={600}>
        <PackagesSection />
      </SectionWrapper>
      <SectionWrapper id="section-5" delay={800}>
        <ReviewSection />
      </SectionWrapper>
    </main>
  );
}

export default MainPage;
