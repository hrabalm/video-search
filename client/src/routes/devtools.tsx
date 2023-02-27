import Title from "../components/Title";
import { Button } from "@mui/material";
import { indexNewFiles, reindexAll } from "../lib/utils";

async function callIndexNewFiles() {
  await indexNewFiles();
  console.log("Indexing queued...");
}

async function callReindexAll() {
  await reindexAll();
  console.log("Reindixing queued/..");
}

function IndexNewFilesButton() {
  // FIXME: ideally, the button would be disabled while indexing/reindexing is going on, also probaly makes sense pressing this only once
  return (
    <Button onClick={() => callIndexNewFiles()} variant="outlined">
      Index New Files
    </Button>
  );
}

function ReindexAllButton() {
  // FIXME: ideally, the button would be disabled while indexing/reindexing is going on, also probaly makes sense pressing this only once
  return (
    <Button onClick={() => callReindexAll()} variant="outlined">
      Reindex All
    </Button>
  );
}

export default function Development() {
  return (
    <>
      <Title title="Development Tools" />
      <IndexNewFilesButton />
      <ReindexAllButton />
    </>
  );
}
