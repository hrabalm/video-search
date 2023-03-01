import axios from "axios";

export function buildApiUrl(stem: string) {
  return `${process.env.REACT_APP_API_URI}${stem}`;
}

export async function fetchAvailableTags() {
  const response = await axios("/api/v2/tags");
  return response.data;
}

export async function fetchVideosFiltered(
  tags: string[],
  itemsPerPage: number,
  pageNumber: number
) {
  const response = await axios.post("/api/v2/videos-by-tags", {
    tags,
    items_per_page: itemsPerPage,
    page_number: pageNumber,
  });
  return response.data;
}

export async function getVideoCount(tags: string[] = []) {
  const response = await axios.post("/api/v2/videos-count", { tags });
  return response.data;
}

export async function getVideo(videoId: string) {
  const response = await axios(`/api/v2/videos/${videoId}`);
  return response.data;
}

export async function indexNewFiles() {
  const response = await axios.post(`/api/v2/index-new-files`);
  return response.data;
}

export async function reindexAll() {
  const response = await axios.post(`/api/v2/reindex-all`);
  return response.data;
}

export async function debugDeleteStatus() {
  const response = await axios.post("/api/v2/debug-delete-status");
  return response.data;
}
