import React from 'react';
import Button from '@mui/material/Button';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import CssBaseline from '@mui/material/CssBaseline';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import './App.css';
import { Container, Divider, Drawer, IconButton, InputBase, List, ListItem, ListItemText, Toolbar } from '@mui/material';

function SearchBar() {
  return (
    <Box>
      <Paper style={{ display: "flex", alignItems: "center" }} sx={{ m: 1 }}>
        <TextField sx={{ m: 1, flex: 1 }} placeholder="Search"></TextField>
        <Button>Search</Button>
      </Paper>
    </Box>
  );
}

function SearchView() {
  return (
    <Box>
      <SearchBar />
    </Box>
  );
}

function App() {
  const darkTheme = createTheme({
    palette: {
      mode: 'dark',
    },
  });
  const drawerWidth = 240;
  return (
    <ThemeProvider theme={darkTheme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <header className="App-header">
        </header>
        <Drawer
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: drawerWidth,
              boxSizing: 'border-box',
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
            <ListItem button key={"Search by tag"}>
              <ListItemText primary={"Search by tag"} />
            </ListItem>
          </List>
          <Divider />
        </Drawer>
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            overflow: 'auto',
          }}
        >
          <SearchView />
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;