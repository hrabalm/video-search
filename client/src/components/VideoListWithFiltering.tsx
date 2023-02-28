import Box from "@mui/material/Box";

import { useState, useEffect } from "react";
import {
  Dialog,
  Paper,
  Table,
  TableHead,
  TableCell,
  TableRow,
  TableBody,
  Link,
  Button,
  Typography,
  TableContainer,
  Autocomplete,
  TextField,
  Grid,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { Link as RouterLink } from "react-router-dom";

import { fetchAvailableTags, fetchVideosFiltered } from "../lib/utils";
import { VideoRecord } from "../lib/types";

export default function VideoListWithFiltering() {
  const [data, setData]: [{ videos: VideoRecord[] }, any] = useState({
    videos: [],
  });
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedTags, setSelectedTags]: [string[], any] = useState([]);
  const [availableTags, setAvailableTags]: [string[], any] = useState([]);
  const [dialogActiveTag, setDialogActiveTag]: [string, any] = useState("");

  useEffect(() => {
    const tags = fetchAvailableTags();
    tags.then((x) => {
      console.log(x);
      setAvailableTags(x.tags);
    });
  }, [setAvailableTags]);

  useEffect(() => {
    const videos = fetchVideosFiltered(selectedTags);
    videos.then(setData);
  }, [selectedTags]);

  const handleClickFilter = () => {
    setDialogOpen(true);
  };

  const handleClearFilters = () => {
    setSelectedTags([]);
  };

  const handleRefresh = () => {
    const videos = fetchVideosFiltered(selectedTags);
    videos.then(setData);
  };

  const handleFiltersDialogClose = () => {
    setDialogOpen(false);
  };

  const activeFiltersText = (count: number) => {
    if (count === 0) {
      return "No Active Filters.";
    } else if (count === 1) {
      return "1 Active Filter.";
    } else {
      return `${count} Active Filters.`;
    }
  };

  return (
    <>
      <TableContainer component={Paper} sx={{ p: 1 }}>
        <Grid container sx={{ alignItems: "center" }}>
          <Grid item xs={3} sx={{ textAlign: "center" }}>
            <Typography>{activeFiltersText(selectedTags.length)}</Typography>
          </Grid>
          <Grid item xs={9} sx={{ textAlign: "right" }}>
            <Button
              variant="outlined"
              onClick={handleClickFilter}
              sx={{ m: 0.5 }}
            >
              Edit Filters
            </Button>
            <Button
              variant="outlined"
              onClick={handleClearFilters}
              sx={{ m: 0.5 }}
            >
              Clear Filters
            </Button>
            <Button variant="outlined" onClick={handleRefresh} sx={{ m: 0.5 }}>
              Refresh
            </Button>
          </Grid>
        </Grid>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Path</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.hasOwnProperty("videos") &&
              data.videos.map((row) => (
                <TableRow key={row.filenames[0]}>
                  <TableCell>
                    <Link
                      component={RouterLink}
                      to={`/videos/${row["_id"]["$oid"]}`}
                    >
                      {row.filenames[0]}
                    </Link>
                  </TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog
        open={dialogOpen}
        onClose={handleFiltersDialogClose}
        maxWidth="md"
        fullWidth
      >
        <Box sx={{ m: 1, minHeight: 400 }}>
          <Grid
            container
            sx={{ textAlign: "center", alignItems: "center", display: "flex" }}
          >
            <Grid item xs={10}>
              <Autocomplete
                value={dialogActiveTag}
                disablePortal
                options={availableTags}
                renderInput={(params) => <TextField {...params} label="Tag" />}
                onChange={(_, value) => {
                  if (value != null) {
                    setDialogActiveTag(value);
                  }
                }}
              />
            </Grid>
            <Grid item xs={2}>
              <Box>
                <Button
                  key={selectedTags.join("+")}
                  size="large"
                  variant="contained"
                  disabled={!availableTags.includes(dialogActiveTag)}
                  onClick={() => {
                    if (
                      availableTags.length > 0 &&
                      availableTags.includes(dialogActiveTag)
                    ) {
                      setSelectedTags(
                        Array.from(
                          new Set([dialogActiveTag, ...selectedTags])
                        ).sort()
                      );
                      setDialogActiveTag("");
                    }
                  }}
                >
                  Add
                </Button>
              </Box>
            </Grid>
          </Grid>
          <Typography>Active Filters:</Typography>
          <TableContainer component={Paper}>
            <Table sx={{ p: 1 }}>
              <TableHead>
                <TableRow>
                  <TableCell>Tag</TableCell>
                  <TableCell></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {selectedTags.map((tag) => (
                  <TableRow>
                    <TableCell>{tag}</TableCell>
                    <TableCell>
                      <Button variant="outlined" startIcon={<DeleteIcon />}>
                        Delete
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      </Dialog>
    </>
  );
}
