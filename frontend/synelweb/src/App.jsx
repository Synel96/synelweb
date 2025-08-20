import { CssBaseline, CssVarsProvider } from "@mui/joy";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/navbar/Navbar";
import Footer from "./components/footer/Footer";
import theme from "./themes/theme";
import MainPage from "./pages/MainPage";
import ProjectsPage from "./pages/ProjectsPage";
import ContactsPage from "./pages/ContactsPage";

function App() {
  return (
    <CssVarsProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/projektek" element={<ProjectsPage />} />
          <Route path="/elerhetoseg" element={<ContactsPage />} />
        </Routes>
        <Footer />
      </BrowserRouter>
    </CssVarsProvider>
  );
}

export default App;
