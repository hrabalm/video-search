import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Root from "./routes/root";
import DevTools from './routes/devtools';
import SearchByTag from './routes/search-by-tags';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      {
        path: "search-by-tag/",
        index: true,
        element: <SearchByTag />
      },
      {
        path: "search-by-image/",
        element: <h1>TODO: Search by image</h1>
      },
      {
        path: "status/",
        element: <h1>TODO: Status (how is the indexing going?)</h1>
      },
      {
        path: "settings/",
        element: <h1>TODO: Settings</h1>
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
