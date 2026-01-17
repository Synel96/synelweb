import {
  Box,
  ListItemButton,
  IconButton,
  Drawer,
  List,
  ListItem,
} from "@mui/joy";
import MenuIcon from "@mui/icons-material/Menu";
import { useColorScheme } from "@mui/joy";
import { useState } from "react";
import useMediaQuery from "@mui/material/useMediaQuery";
import { Link } from "react-router-dom"; // React Router import

function Menu() {
  const { mode } = useColorScheme();
  const [open, setOpen] = useState(false);
  const isMobile = useMediaQuery("(max-width:600px)");

  const menuItems = [
    { label: "Főoldal", href: "/" },
    { label: "Projektek", href: "/projektek" },
    { label: "Vélemények", href: "/velemenyek" },
    { label: "Szolgáltatások", href: "/szolgaltatasok" },
    { label: "Elérhetőség", href: "/elerhetoseg" },
    { label: "Rólam", href: "/rolam" },
  ];

  if (isMobile) {
    return (
      <>
        <IconButton
          aria-label="Mobilmenü megnyitása"
          onClick={() => setOpen(true)}
        >
          <MenuIcon />
        </IconButton>
        <Drawer
          open={open}
          onClose={() => setOpen(false)}
          aria-label="Mobil navigációs menü"
        >
          <nav aria-label="Fő navigáció">
            <List>
              {menuItems.map(({ label, href }) => (
                <ListItem key={label}>
                  <ListItemButton
                    component={Link} // React Router Link
                    to={href}
                    sx={{
                      borderRadius: "24px",
                      px: 3,
                      py: 1,
                      fontWeight: 500,
                      fontSize: "1rem",
                      bgcolor: "transparent",
                      color: mode === "dark" ? "#fff" : "#121212",
                      "&:hover": {
                        bgcolor: mode === "dark" ? "#fff" : "#f5f5f5",
                        color: mode === "dark" ? "#121212" : "#1976d2",
                      },
                      transition: "all 0.2s",
                      boxShadow: "none",
                      border: "none",
                    }}
                    onClick={() => setOpen(false)}
                    aria-label={label}
                  >
                    {label}
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          </nav>
        </Drawer>
      </>
    );
  }

  // Desktop nézet
  return (
    <nav aria-label="Fő navigáció">
      <Box sx={{ display: "flex", gap: 2 }}>
        {menuItems.map(({ label, href }) => (
          <ListItemButton
            key={label}
            component={Link} // React Router Link
            to={href}
            sx={{
              borderRadius: "24px",
              px: 3,
              py: 1,
              fontWeight: 500,
              fontSize: "1rem",
              bgcolor: "transparent",
              color: mode === "dark" ? "#fff" : "#121212",
              "&:hover": {
                bgcolor: mode === "dark" ? "#fff" : "#f5f5f5",
                color: mode === "dark" ? "#121212" : "#1976d2",
              },
              transition: "all 0.2s",
              boxShadow: "none",
              border: "none",
            }}
            aria-label={label}
          >
            {label}
          </ListItemButton>
        ))}
      </Box>
    </nav>
  );
}

export default Menu;
