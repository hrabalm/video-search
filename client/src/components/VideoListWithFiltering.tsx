import Box from "@mui/material/Box";

import { useState, useEffect } from "react";
import {
  Paper,
  Table,
  TableHead,
  TableCell,
  TableRow,
  TableBody,
  Link,
  Button,
} from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import { Dialog } from "@mui/material";

import { fetchAvailableTags, fetchVideosFiltered } from "../lib/utils";
import { VideoRecord } from "../lib/types";

function ListAvailableTags() {
  const [data, setData] = useState({ tags: [] });

  useEffect(() => {
    fetchAvailableTags().then(setData);
  }, []);

  return (
    <Box>
      <div>Available tags:</div>
      <ul>
        {data.tags.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </Box>
  );
}

function ResultsTable({ tags }: { tags: string[] }) {
  const [data, setData]: [{ videos: VideoRecord[] }, any] = useState({
    videos: [],
  });
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    const videos = fetchVideosFiltered(tags);
    videos.then(setData);
  }, []);

  const handleClickFilter = () => {
    setDialogOpen(true);
  };

  const handleDeleteFilter = () => {
    // TODO: implement
  };

  const handleRefresh = () => {
    // TODO: implement
  };

  const handleFiltersDialogClose = () => {
    setDialogOpen(false);
  };

  return (
    <>
      <Paper>
        <Button variant="outlined" onClick={handleClickFilter} sx={{ m: 0.5 }}>
          Edit Filters
        </Button>
        <Button variant="outlined" onClick={handleDeleteFilter} sx={{ m: 0.5 }}>
          Delete Filters
        </Button>
        <Button variant="outlined" onClick={handleRefresh} sx={{ m: 0.5 }}>
          Refresh
        </Button>
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
      </Paper>

      <Dialog open={dialogOpen} onClose={handleFiltersDialogClose}>
        <ListAvailableTags />
      </Dialog>
    </>
  );
}

export default function VideoListWithFiltering() {
  return (
    <>
      <Box>
        <ResultsTable tags={[]} />
      </Box>
    </>
  );
}
