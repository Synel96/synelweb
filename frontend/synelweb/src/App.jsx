import { CssBaseline, CssVarsProvider } from "@mui/joy";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/navbar/Navbar";
import Footer from "./components/footer/Footer";

import theme from "./theme"; // ha van saját theme.js

function App() {
  return (
    <CssVarsProvider theme={theme}>
      <CssBaseline />
      <Navbar />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<h1>Főoldal</h1>} />
        </Routes>
      </BrowserRouter>
      <Footer />
    </CssVarsProvider>
  );
}

export default App;
