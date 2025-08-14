import { useColorScheme } from "@mui/joy";

export default function useDarkMode() {
  const { mode, setMode } = useColorScheme();
  return { mode, setMode };
}
