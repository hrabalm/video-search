import Title from "../components/Title";
import { Form, useLoaderData } from "react-router-dom";
import { getVideo } from "../lib/utils";
import { Chip, Grid, Paper, styled, Typography } from "@mui/material";
import _ from "lodash";

export async function loader({ params }: { params: any }) {
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

export default function VideoDetail() {
  const video: any = useLoaderData();
  const tags_by_tagger = _.groupBy(video.video.tags, (tag) => tag.model);

  const CHIP_MARGIN = 0.3;

  return (
    <>
      <Title title="Video Detail" />
      {/* {JSON.stringify(video, null, 4)} */}
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
      <Typography>Tags:</Typography>
      <Grid container spacing={2}>
        <Grid item xs={4}>
          <Item>
            {Object.entries(tags_by_tagger).map(([model, tags]) => {
              return <Chip label={model} sx={{ margin: CHIP_MARGIN }} />;
            })}
          </Item>
        </Grid>
        <Grid item xs={8}>
          <Item>
            {Object.entries(tags_by_tagger).map(([model, tags]) => {
              return tags
                .filter((tag) => tag.conf >= 0.75)
                .map((tag) => {
                  return <Chip label={tag.tag} sx={{ margin: CHIP_MARGIN }} />;
                });
            })}
          </Item>
        </Grid>
      </Grid>
    </>
  );
}
