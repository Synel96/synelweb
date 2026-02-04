import { CssBaseline, CssVarsProvider } from "@mui/joy";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { lazy, Suspense } from "react";
import Navbar from "./components/navbar/Navbar";
import Footer from "./components/footer/Footer";

// Lazy load pages for code splitting
const MainPage = lazy(() => import("./pages/MainPage"));
const ProjectsPage = lazy(() => import("./pages/projektek/+Page.jsx"));
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
    minHeight: '60vh'
  }}>
    <div style={{
      width: '40px',
      height: '40px',
      border: '3px solid #e0e0e0',
      borderTop: '3px solid #1976d2',
      borderRadius: '50%',
      animation: 'spin 0.8s linear infinite'
    }}></div>
    <style>{`
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    `}</style>
  </div>
);

function App() {
  return (
    <CssVarsProvider defaultMode="dark">
      <CssBaseline />
      <BrowserRouter>
        <div style={{ 
          display: 'flex', 
          flexDirection: 'column', 
          minHeight: '100vh' 
        }}>
          <Navbar />
          <main style={{ flex: 1 }}>
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
          </main>
          <Footer />
        </div>
      </BrowserRouter>
    </CssVarsProvider>
  );
}

export default App;
