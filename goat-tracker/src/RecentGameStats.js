import React, { useEffect, useState } from 'react';
import "./RecentGameStats.css";

function RecentGameStats() {
    const PATHWAY = 'http://127.0.0.1:5000/api/lebron/recent-game';
    const [recentGameStats, setRecentGameStats] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(PATHWAY);
                const data = await response.json();
                setRecentGameStats(data);
                console.log(data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchData();
    }, []);

    return (
        <div className="RecentGameStats">
            <p>In Lebron James' most recent game, he scored {recentGameStats.PTS} points, grabbed {recentGameStats.REB} boards, and assisted {recentGameStats.AST} times in {recentGameStats.MIN} minutes in a {recentGameStats.WL}.
            </p>
        </div>
    )
}

export default RecentGameStats;
