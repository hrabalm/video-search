import Title from "../components/Title";
import { Button } from "@mui/material";
import { reindexAll } from "../lib/utils";

async function callReindexAll() {
  await reindexAll();
  console.log("Reindixing done");
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
      <ReindexAllButton />
    </>
  );
}
