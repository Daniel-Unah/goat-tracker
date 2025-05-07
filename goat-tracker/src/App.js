import React from "react";
import CareerStats from "./CareerStats.js";
import RecentGameStats from "./RecentGameStats.js";
import RandomNotableGameStats from "./RandomNotableGame.js";
import "./App.css";
import "./CareerStats.css";
import "./RecentGameStats.css";
import "./RandomNotableGame.css";

const App = () => {
  return (
    <div>
      <CareerStats />
      <RecentGameStats />
      <RandomNotableGameStats />
    </div>
  );
};

export default App;
