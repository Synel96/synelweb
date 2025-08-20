import { CssBaseline, CssVarsProvider } from "@mui/joy";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/navbar/Navbar";
import Footer from "./components/footer/Footer";
import MainPage from "./pages/MainPage";
import ProjectsPage from "./pages/ProjectsPage";
import ContactsPage from "./pages/ContactsPage";
import ReviewsPage from "./pages/ReviewsPage";
import PackagesPage from "./pages/PackagesPage";

function App() {
  return (
    <CssVarsProvider>
      <CssBaseline />
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/projektek" element={<ProjectsPage />} />
          <Route path="/elerhetoseg" element={<ContactsPage />} />
          <Route path="/velemenyek" element={<ReviewsPage />} />
          <Route path="/szolgaltatasok" element={<PackagesPage />} />
        </Routes>
        <Footer />
      </BrowserRouter>
    </CssVarsProvider>
  );
}

export default App;
