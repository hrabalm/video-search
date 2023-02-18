import Title from "../components/Title";
import { Form, useLoaderData } from "react-router-dom";
import { getVideo } from "../lib/utils";

export async function loader({ params }) {
  const videoId = params.videoId;
  return await getVideo(videoId);
}

export default function VideoDetail() {
  const video = useLoaderData();
  console.log(video);
  return (
    <>
      <Title title="Video Detail" />
      {JSON.stringify(video, null, 4)}
    </>
  );
}
