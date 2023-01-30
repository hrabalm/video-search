import Box from '@mui/material/Box';
import SearchBar from './SearchBar';

import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AvailableTags() {
    const [data, setData] = useState({ tags: [] });

    useEffect(() => {
        const fetchData = async () => {
            const result = await axios('api/v2/tags');

            console.log(result);
            console.log(result.data);
            setData(result.data);
        };
        fetchData();
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
        const fetchData = async () => {
            const result = await axios.post('api/v2/videos-by-tags', {tags: ['web_site']});

            console.log(result);
            console.log(result.data);
            setData(result.data);
        };
        fetchData();
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

export default function SearchView() {
    return (
        <Box>
            <SearchBar />
            <AvailableTags />
            <MockSearchResults />
        </Box>
    );
}
