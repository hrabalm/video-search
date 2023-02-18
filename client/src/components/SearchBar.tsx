import React from "react";
import Button from "@mui/material/Button";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";

export default function SearchBar() {
  return (
    <Box>
      <Paper
        style={{
          display: "flex",
          alignItems: "left",
          flexDirection: "column",
        }}
        sx={{ p: 1 }}
      >
        <Box style={{ display: "flex", flexDirection: "row" }}>
          <TextField sx={{ m: 1, flex: 1 }} placeholder="Search"></TextField>
          <Button>Search</Button>
        </Box>
        <Box style={{ display: "flex", flexDirection: "row" }}>
          <Typography>Selected tags:</Typography>
        </Box>
      </Paper>
    </Box>
  );
}
