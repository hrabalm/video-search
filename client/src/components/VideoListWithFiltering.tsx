import Box from '@mui/material/Box';
import SearchBar from './SearchBar';

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, TableHead, TableCell, TableRow, TableBody, Link } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

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

function ResultsTable({ tags }: any) {
    const [data, setData] = useState({ videos: [] });

    useEffect(() => {
        const videos = fetchVideosFiltered(tags);
        videos.then(setData);
    }, []);

    return (
        <Table>
            <TableHead>
                <TableRow>
                    <TableCell>Path</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {data.hasOwnProperty('videos') && data.videos.map((row) => (
                    <TableRow key={row.filenames[0]}>
                        <TableCell>
                            <Link component={RouterLink} to={`/videos/${row["_id"]["$oid"]}`}>
                                {row.filenames[0]}
                            </Link>
                        </TableCell>
                    </TableRow>
                ))}

            </TableBody>
        </Table>
    );
}

export default function VideoListWithFiltering() {
    return (
        <Box>
            <SearchBar />
            <ResultsTable tags={[]} />
            <ListAvailableTags />
        </Box>
    );
}
