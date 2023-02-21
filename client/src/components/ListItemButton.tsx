import { Link } from "react-router-dom";
import { ListItemText, ListItemButton } from "@mui/material";

export default function DrawerListLink({
  text,
  absolute,
}: {
  text: string;
  absolute: string;
}) {
  return (
    <ListItemButton key={text} component={Link} to={absolute}>
      <ListItemText primary={text} />
    </ListItemButton>
  );
}
