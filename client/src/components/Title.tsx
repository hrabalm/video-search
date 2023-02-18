import { Typography } from "@mui/material";

export default function Title({ title }: { title: string }) {
  return (
    <Typography component="h2" variant="h3">
      {title}
    </Typography>
  );
}
