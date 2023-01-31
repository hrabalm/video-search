import Box from '@mui/material/Box';
import SearchBar from './SearchBar';

import React, { useState, useEffect } from 'react';
import axios from 'axios';

import { fetchAvailableTags, fetchVideosFiltered } from '../lib/utils';

function ListAvailableTags() {
    const [data, setData] = useState({ tags: [] });

    useEffect(() => {
        fetchAvailableTags().then(setData);
    }, []);

    return (
        <Box>
            <div>Available tags:</div>
            <ul>
                {data.tags.map(item => (
                    <li key={item}>
                        {item}
                    </li>
                ))}
            </ul>
        </Box>
    );
}

function MockSearchResults() {
    const [data, setData] = useState({ videos: [] });

    useEffect(() => {
        const videos = fetchVideosFiltered(['web_site']);
        videos.then(setData);
    }, []);

    return (
        <Box>
            <div>Requested tags:</div>
            <ul>
                {data.videos.map(item => (
                    <li key={JSON.stringify(item)}>
                        {JSON.stringify(item)}
                    </li>
                ))}
            </ul>
            <p>{data.videos.length}</p>
        </Box>
    );
}

function ResultsTable({tags} : any) {
    const [data, setData] = useState({ videos: [] });

    useEffect(() => {
        const videos = fetchVideosFiltered(tags);
        videos.then(setData);
    }, []);

    return (
        <></>
    );
}

export default function VideoListWithFiltering() {
    return (
        <Box>
            <SearchBar />
            <ListAvailableTags />
            <MockSearchResults />
        </Box>
    );
}
