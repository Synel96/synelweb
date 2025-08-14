import { CssBaseline, CssVarsProvider } from "@mui/joy";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/navbar/Navbar";
import Footer from "./components/footer/Footer";
import theme from "./theme";
import MainPage from "./pages/MainPage";

function App() {
  return (
    <CssVarsProvider theme={theme}>
      <CssBaseline />
      <Navbar />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MainPage />} />
        </Routes>
      </BrowserRouter>
      <Footer />
    </CssVarsProvider>
  );
}

export default App;
