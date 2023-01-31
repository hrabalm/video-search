import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Root from "./routes/root";
import DevTools from './routes/devtools';
import SearchByTag from './routes/search-by-tag';
import SearchByImage from './routes/search-by-image';
import Status from './routes/status';
import Settings from './routes/settings';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      {
        path: "search-by-tag?/",
        index: true,
        element: <SearchByTag />
      },
      {
        path: "search-by-image/",
        element: <SearchByImage />
      },
      {
        path: "status/",
        element: <Status />
      },
      {
        path: "settings/",
        element: <Settings />
      },
      {
        path: "devtools/",
        element: <DevTools />
      },
    ],
  },
]);

ReactDOM.render(
  <React.StrictMode>
      <RouterProvider router={router} />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
