import React from "react";
import CareerStats from "./CareerStats.js";
import RecentGameStats from "./RecentGameStats.js";
import "./App.css";
import "./CareerStats.css";

const App = () => {
  return (
    <div>
      <CareerStats />
      <RecentGameStats />
    </div>
  );
};

export default App;
