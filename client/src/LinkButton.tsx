import React from "react";
import Button from "@mui/material/Button";
import { useNavigate } from "react-router";

interface LinkButtonProps {
  link: string;
  text: string;
}

export default function LinkButton(props: LinkButtonProps) {
  let navigate = useNavigate();

  return <Button variant="outlined" sx={{m: 0.5}} onClick={() => navigate(props.link)}>{props.text}</Button>;
}
