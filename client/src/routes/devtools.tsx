import Title from "../components/Title";
import { Button, Stack, Paper, styled } from "@mui/material";
import { indexNewFiles, reindexAll, debugDeleteStatus } from "../lib/utils";

async function callIndexNewFiles() {
  await indexNewFiles();
  console.log("Indexing queued...");
}

async function callReindexAll() {
  await reindexAll();
  console.log("Reindixing queued/..");
}

const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: "left",
  color: theme.palette.text.secondary,
}));

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

function DeleteStatusButton() {
  return (
    <Button
      onClick={() => {
        debugDeleteStatus();
      }}
      variant="outlined"
    >
      Delete Status
    </Button>
  );
}

export default function Development() {
  return (
    <>
      <Title title="Development Tools" />
      <Stack spacing={2}>
        <Item>
          <IndexNewFilesButton />
        </Item>
        <Item>
          <ReindexAllButton />
        </Item>
        <Item>
          <DeleteStatusButton />
        </Item>
      </Stack>
    </>
  );
}
