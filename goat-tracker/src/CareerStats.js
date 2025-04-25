import React, { useEffect, useState } from 'react';
import "./CareerStats.css";

function CareerStats(){
  const PATHWAY = 'http://127.0.0.1:5000/api/lebron/career-stats'
  const [careerStats, setcareerStats] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(PATHWAY);
        const data = await response.json();
        setcareerStats(data);
        console.log(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  // Calculate total stats
  let totalGP = 0;
  let totalPoints = 0;
  let totalRebounds = 0;
  let totalAssists = 0;

  careerStats.forEach((season) => {
    totalGP += season.GP;
    totalPoints += season.PTS;
    totalRebounds += season.REB;
    totalAssists += season.AST;
  });

  return (
    <div className="CareerStats">
      <h1>LeBron James Career Stats</h1>
      <table>
        <thead>
          <tr>
            <th>Games Played</th>
            <th>Points</th>
            <th>Rebounds</th>
            <th>Assists</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{totalGP}</td>
            <td>{totalPoints}</td>
            <td>{totalRebounds}</td>
            <td>{totalAssists}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default CareerStats;