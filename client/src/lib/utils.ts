import axios from 'axios';

export async function fetchAvailableTags() {
    const response = await axios('/api/v2/tags');
    return response.data;
}

export async function fetchVideosFiltered(tags: string[]) {
    const response = await axios.post('/api/v2/videos-by-tags', {tags});
    return response.data;
}

export async function getVideo(videoId: string) {
    const response = await axios(`/api/v2/videos/${videoId}`);
    return response.data;
}

export async function reindexAll() {
    const response = await axios.post(`/api/v2/reindex-all`)
    return response.data
}
