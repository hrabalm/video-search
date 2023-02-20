import Title from "../components/Title";
import { Form, useLoaderData } from "react-router-dom";
import { getVideo } from "../lib/utils";
import { Chip } from "@mui/material";

export async function loader({ params }: { params: any }) {
  const videoId = params.videoId;
  return await getVideo(videoId);
}

export default function VideoDetail() {
  const video: any = useLoaderData();
  return (
    <>
      <Title title="Video Detail" />
      {JSON.stringify(video, null, 4)}
      {
        // TODO: this should be sorted by tag type (which could also be Chip in
        // the left column, its tags would be in right)
        // TODO: tag could be clickable and could contain its explanation page:
        // e.g.: "I think there are lots of frames with cats and the most conf
        // one is in frame 1234."
        video.video.tags.map((tag: any) => {
          return <Chip label={ tag.tag } />
        })
      }
    </>
  );
}
