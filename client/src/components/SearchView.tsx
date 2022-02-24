import Box from '@mui/material/Box';
import SearchBar from './SearchBar';

import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AvailableTags() {
    const [data, setData] = useState({ tags: [] });

    useEffect(() => {
        const fetchData = async () => {
            const result = await axios('api/v1/get-tags');

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
    const [data, setData] = useState({ tags: [] });

    useEffect(() => {
        const fetchData = async () => {
            const result = await axios.post('api/v1/search-by-tags', {requested_tags: ['cat']});

            console.log(result);
            console.log(result.data);
            setData(result.data);
        };
        fetchData();
    }, []);

    return (
        <Box>
            <div>Requested tags:</div>
            <div>{JSON.stringify(data)}</div>
            {/* <ul>
                {data.tags.map(item => (
                    <li key={item}>
                        {item}
                    </li>
                ))}
            </ul> */}
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
