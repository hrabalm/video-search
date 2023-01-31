import axios from 'axios';

export async function fetchAvailableTags() {
    const response = await axios('/api/v2/tags');
    return response.data;
}

export async function fetchVideosFiltered(tags) {
    const response = await axios.post('/api/v2/videos-by-tags', {tags});
    return response.data;
}
