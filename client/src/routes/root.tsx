import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import { Container, Divider, Drawer, List, Toolbar } from "@mui/material";
import Typography from "@mui/material/Typography";
import { Outlet } from "react-router-dom";
import DrawerListLink from "../components/ListItemButton";

export default function Root() {
  const darkTheme = createTheme({
    palette: {
      mode: "dark",
    },
  });
  const drawerWidth = 240;
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Box sx={{ display: "flex" }}>
        <Drawer
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            "& .MuiDrawer-paper": {
              width: drawerWidth,
              boxSizing: "border-box",
            },
          }}
          variant="permanent"
        >
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Video Search
            </Typography>
          </Toolbar>

          <Divider />
          <List>
            <DrawerListLink text="Search by tag" absolute="/search-by-tag/" />
            {/*
            // FIXME: Searching by image is not yet implemented
            <DrawerListLink
              text="Search by image"
              absolute="/search-by-image/"
            />
            */}
            <Divider />
            {/* <DrawerListLink text="Status" absolute="/status/" /> */}
            {/* <DrawerListLink text="Settings" absolute="/settings/" /> */}
            <Divider />
            <DrawerListLink text="DevTools" absolute="/devtools/" />
          </List>
          <Divider />
        </Drawer>
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            overflow: "auto",
          }}
        >
          <Container maxWidth="lg" sx={{ marginTop: 3, marginBot: 3 }}>
            <Outlet />
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}
