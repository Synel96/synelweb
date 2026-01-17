import { CssBaseline, CssVarsProvider } from "@mui/joy";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { lazy, Suspense } from "react";
import Navbar from "./components/navbar/Navbar";
import Footer from "./components/footer/Footer";

// Lazy load pages for code splitting
const MainPage = lazy(() => import("./pages/MainPage"));
const ProjectsPage = lazy(() => import("./pages/ProjectsPage"));
const ContactsPage = lazy(() => import("./pages/ContactsPage"));
const ReviewsPage = lazy(() => import("./pages/ReviewsPage"));
const PackagesPage = lazy(() => import("./pages/PackagesPage"));
const AboutPage = lazy(() => import("./pages/AboutPage"));

// Loading fallback component
const PageLoader = () => (
  <div style={{ 
    display: 'flex', 
    justifyContent: 'center', 
    alignItems: 'center', 
    minHeight: '60vh',
    fontSize: '1.2rem',
    color: '#1976d2'
  }}>
    Betöltés...
  </div>
);

function App() {
  return (
    <CssVarsProvider>
      <CssBaseline />
      <BrowserRouter>
        <Navbar />
        <Suspense fallback={<PageLoader />}>
          <Routes>
            <Route path="/" element={<MainPage />} />
            <Route path="/projektek" element={<ProjectsPage />} />
            <Route path="/elerhetoseg" element={<ContactsPage />} />
            <Route path="/velemenyek" element={<ReviewsPage />} />
            <Route path="/szolgaltatasok" element={<PackagesPage />} />
            <Route path="/rolam" element={<AboutPage />} />
          </Routes>
        </Suspense>
        <Footer />
      </BrowserRouter>
    </CssVarsProvider>
  );
}

export default App;
