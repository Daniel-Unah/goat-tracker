import React, { useEffect, useState } from 'react';
import "./RecentGameStats.css";

function RecentGameStats() {
    const [recentGameStats, setRecentGameStats] = useState([]);
    const [seasonType, setSeasonType] = useState("Regular Season");

    useEffect(() => {
        const PATHWAY = `https://goat-tracker-backend-production.up.railway.app/api/lebron/recent-game?season_type=${seasonType}`;
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
    }, [seasonType]); // this makes the data refresh whenever seasonType changes

    const matchup = recentGameStats.MATCHUP || "";
    const opponent = matchup.split(" ")[2];

    return (
        <>
            <div className="toggle">
                <select value={seasonType} onChange={(e) => setSeasonType(e.target.value)}>
                    <option value="Regular Season">Regular Season</option>
                    <option value="Playoffs">Playoffs</option>
                </select>
            </div>

            <div className="RecentGameStats">
                <p>In Lebron James' most recent game, he scored {recentGameStats.PTS} points, grabbed {recentGameStats.REB} boards, and assisted {recentGameStats.AST} times in {recentGameStats.MIN} minutes in a {recentGameStats.WL} vs {opponent} in the {seasonType}.
                </p>
            </div>
        </>
    )
}

export default RecentGameStats;
