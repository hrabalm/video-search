import Button from "@mui/material/Button";

interface DownloadButtonProps {
  link: string;
  text: string;
}

export default function DownloadButton(props: DownloadButtonProps) {
  return (
    <Button
      variant="outlined"
      sx={{ m: 0.5 }}
      download
      href={props.link}
      target="_blank"
      rel="noopener noreferrer"
    >
      {props.text}
    </Button>
  );
}
