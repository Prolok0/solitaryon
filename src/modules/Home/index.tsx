import React, { useEffect } from 'react';
import { io } from 'socket.io-client';

const Home = () => {
    const socket = io('/api/socket');

    useEffect(() => {
        socket.on('connect', () => {
            console.log("Connected! " + socket.id);
        });
    });

    return (
        <>
        Hi
        </>
    );
}

export default Home;