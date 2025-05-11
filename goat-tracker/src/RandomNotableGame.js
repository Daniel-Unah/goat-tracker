import React, { useEffect, useState } from 'react';
import "./RandomNotableGame.css";

function RandomNotableGameStats() {
    const [randomNotableGameStats, setRandomNotableGameStats] = useState([]);
    const [seasonType, setSeasonType] = useState("Regular Season");

    useEffect(() => {
        const PATHWAY = `https://goat-tracker-backend-production.up.railway.app/api/lebron/random-game?season_type=${seasonType}`;
        const fetchData = async () => {
            try {
                const response = await fetch(PATHWAY);
                const data = await response.json();
                setRandomNotableGameStats(data);
                console.log(data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchData();
    }, [seasonType]); // this makes the data refresh whenever seasonType changes

    const matchup = randomNotableGameStats.MATCHUP || "";
    const opponent = matchup.split(" ")[2];

    return (
        <>
            <div className="toggle">
                <select value={seasonType} onChange={(e) => setSeasonType(e.target.value)}>
                    <option value="Regular Season">Regular Season</option>
                    <option value="Playoffs">Playoffs</option>
                </select>
            </div>

            <div className="RandomNotableGameStats">
                <p>On {randomNotableGameStats.GAME_DATE}, LeBron James scored {randomNotableGameStats.PTS} points, grabbed {randomNotableGameStats.REB} boards, and assisted {randomNotableGameStats.AST} times in {randomNotableGameStats.MIN} minutes in a {randomNotableGameStats.WL} vs {opponent} in the {seasonType}.</p>
            </div>
        </>
    )
}

export default RandomNotableGameStats;
