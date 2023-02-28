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
  Stack,
  Toolbar,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { Link as RouterLink } from "react-router-dom";

import { fetchAvailableTags, fetchVideosFiltered } from "../lib/utils";
import { VideoRecord } from "../lib/types";
import { styled } from "@mui/material/styles";

const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  padding: theme.spacing(1),
}));

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
      <Stack spacing={2}>
        <Item>
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
              <Button
                variant="outlined"
                onClick={handleRefresh}
                sx={{ m: 0.5 }}
              >
                Refresh
              </Button>
            </Grid>
          </Grid>
        </Item>
        <Item>
          <Toolbar
            sx={{
              pl: { sm: 2 },
              pr: { xs: 1, sm: 1 },
            }}
          >
            <Typography
              sx={{ flex: "1 1 100%" }}
              variant="h6"
              id="tableTitle"
              component="div"
            >
              Videos
            </Typography>
          </Toolbar>
          <TableContainer>
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
            <Grid container sx={{ alignItems: "center", mt: 1 }}>
              <Grid item xs={3} sx={{ textAlign: "center" }}>
                <Typography>Showing {data.videos.length} results.</Typography>
              </Grid>
            </Grid>
          </TableContainer>
        </Item>

        <Dialog
          open={dialogOpen}
          onClose={handleFiltersDialogClose}
          maxWidth="md"
          fullWidth
        >
          <Box sx={{ m: 1, minHeight: 400 }}>
            <Stack spacing={2}>
              <Item>
                <Grid
                  container
                  sx={{
                    textAlign: "center",
                    alignItems: "center",
                    display: "flex",
                  }}
                >
                  <Grid item xs={10}>
                    <Autocomplete
                      value={dialogActiveTag}
                      disablePortal
                      options={availableTags}
                      renderInput={(params) => (
                        <TextField {...params} label="Add Filter" />
                      )}
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
              </Item>
              <Item>
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
                        <TableRow key={tag}>
                          <TableCell>{tag}</TableCell>
                          <TableCell>
                            <Button
                              variant="outlined"
                              startIcon={<DeleteIcon />}
                              onClick={() => {
                                setSelectedTags(
                                  selectedTags.filter(
                                    (element) => element !== tag
                                  )
                                );
                              }}
                            >
                              Delete
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                      {selectedTags.length === 0 && (
                        <TableRow>
                          <TableCell colSpan={2} sx={{ textAlign: "center" }}>
                            No Active Filters
                          </TableCell>
                        </TableRow>
                      )}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Item>
            </Stack>
          </Box>
        </Dialog>
      </Stack>
    </>
  );
}
