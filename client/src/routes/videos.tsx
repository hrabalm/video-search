import Title from "../components/Title";
import React from "react";
import { useLoaderData } from "react-router-dom";
import { getVideo } from "../lib/utils";
import {
  Box,
  Chip,
  Grid,
  Paper,
  styled,
  TextField,
  Typography,
  Button,
  Tab,
  Tabs,
} from "@mui/material";
import _ from "lodash";
import DownloadButton from "../components/DownloadButton";
import { VideoTag } from "../lib/types";
import { Dictionary } from "lodash";

const TAG_MIN_CONF = 0.75;
const CHIP_MARGIN = 0.3;

export async function loader({ params }: { params: { videoId: string } }) {
  const videoId = params.videoId;
  return await getVideo(videoId);
}

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: "center",
  color: theme.palette.text.secondary,
}));

function TabPanel({
  children,
  index,
  value,
  ...other
}: {
  children?: React.ReactNode;
  index: number;
  value: number;
}) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function TagsTable({
  tags_by_tagger,
}: {
  tags_by_tagger: Dictionary<VideoTag[]>;
}) {
  return (
    <Grid container spacing={2}>
      {Object.entries(tags_by_tagger).map(([model, tags], i) => {
        return (
          <React.Fragment key={i}>
            <Grid item xs={4}>
              <Item>
                <Chip label={model} sx={{ margin: CHIP_MARGIN }} />
              </Item>
            </Grid>
            <Grid item xs={8}>
              <Item>
                {tags
                  .filter((tag: VideoTag) => tag.conf >= TAG_MIN_CONF)
                  .map((tag: VideoTag) => {
                    return (
                      <Chip
                        key={tag.tag}
                        label={tag.tag}
                        sx={{ margin: CHIP_MARGIN }}
                      />
                    );
                  })}
              </Item>
            </Grid>
          </React.Fragment>
        );
      })}
    </Grid>
  );
}

export default function VideoDetail() {
  const video: any = useLoaderData();
  const tags_by_tagger: Dictionary<VideoTag[]> = _.groupBy(
    video.video.tags,
    (tag) => tag.model
  );

  // FIXME: this should be absolute URL to be useful
  const base = "http://localhost:8080"; // TODO: remove
  const url = base + `/api/v2/source-file/${video.video._id["$oid"]}`;

  const [tabValue, setTabValue] = React.useState(0);
  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <>
      <Title title="Video Detail" />
      {
        // TODO: this should be sorted by tag type (which could also be Chip in
        // the left column, its tags would be in right)
        // TODO: tag could be clickable and could contain its explanation page:
        // e.g.: "I think there are lots of frames with cats and the most conf
        // one is in frame 1234."
        // video.video.tags.map((tag: any) => {
        //   return <Chip label={ tag.tag } />
        // })
      }
      <Grid container>
        <Grid item xs sx={{ m: 1 }}>
          <TextField
            id="url-textfield"
            label="Video URL"
            defaultValue={url}
            variant="outlined"
            size="small"
            InputProps={{ readOnly: true }}
            fullWidth
            onFocus={(event) => {
              event.target.select();
            }}
          />
        </Grid>
        <Grid item xs="auto" sx={{ m: 1 }}>
          <Button
            variant="outlined"
            sx={{ m: 0.5 }}
            onClick={() => navigator.clipboard.writeText(url)}
          >
            Copy URL
          </Button>
        </Grid>
        <Grid item xs="auto" sx={{ m: 1 }}>
          <DownloadButton text="Download" link={url} />
        </Grid>
      </Grid>
      <Tabs value={tabValue} onChange={handleChange} centered>
        <Tab label="Tags" />
        <Tab label="Raw" />
      </Tabs>
      <TabPanel value={tabValue} index={0}>
        <Typography>Tags:</Typography>
        <TagsTable tags_by_tagger={tags_by_tagger} />
      </TabPanel>
      <TabPanel value={tabValue} index={1}>
        <Paper>
          <Typography>
            <pre>{JSON.stringify(video, null, 4)}</pre>
          </Typography>
        </Paper>
      </TabPanel>
    </>
  );
}
