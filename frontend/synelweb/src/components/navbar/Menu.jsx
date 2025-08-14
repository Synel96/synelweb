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
import useMediaQuery from "@mui/material/useMediaQuery"; // telepítsd: npm install @mui/material

function Menu() {
  const { mode } = useColorScheme();
  const [open, setOpen] = useState(false);
  const isMobile = useMediaQuery("(max-width:600px)");

  const menuItems = [
    "Főoldal",
    "Projektek",
    "Vélemények",
    "Szolgáltatások",
    "Elérhetőség",
  ];

  if (isMobile) {
    return (
      <>
        <IconButton onClick={() => setOpen(true)}>
          <MenuIcon />
        </IconButton>
        <Drawer open={open} onClose={() => setOpen(false)}>
          <List>
            {menuItems.map((label) => (
              <ListItem key={label}>
                <ListItemButton
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
                >
                  {label}
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Drawer>
      </>
    );
  }

  // Desktop nézet
  return (
    <Box sx={{ display: "flex", gap: 2 }}>
      {menuItems.map((label) => (
        <ListItemButton
          key={label}
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
        >
          {label}
        </ListItemButton>
      ))}
    </Box>
  );
}

export default Menu;
