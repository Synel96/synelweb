import { CssBaseline, CssVarsProvider } from "@mui/joy";
import { CacheProvider } from "@emotion/react";
import Navbar from "../components/navbar/Navbar";
import Footer from "../components/footer/Footer";
import createEmotionCache from "../utils/createEmotionCache";

const clientSideEmotionCache = createEmotionCache();

export default function Layout({
  children,
  emotionCache = clientSideEmotionCache,
}) {
  return (
    <CacheProvider value={emotionCache}>
      <CssVarsProvider defaultMode="dark">
        <CssBaseline />
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            minHeight: "100vh",
          }}
        >
          <Navbar />
          <main style={{ flex: 1 }}>{children}</main>
          <Footer />
        </div>
      </CssVarsProvider>
    </CacheProvider>
  );
}
