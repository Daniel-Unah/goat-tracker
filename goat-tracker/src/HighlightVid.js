import React, { useEffect, useState } from 'react';
import "./HighlightVid.css";

function HighlightVid() {
  const VIDEO_PATH = 'https://goat-tracker-backend-production.up.railway.app/api/lebron/random-video';
  const [videoId, setVideoId] = useState('');

  useEffect(() => {
    const fetchVideo = async () => {
      try {
        const response = await fetch(VIDEO_PATH);
        const data = await response.json();
        setVideoId(data.video_id);
      } catch (error) {
        console.error('Error fetching video:', error);
      }
    };

    fetchVideo();
  }, []);

  return (
    <div className="highlight-container">
      <h2>LeBron Video of the Day</h2>
      {videoId ? (
        <iframe
          width="560"
          height="315"
          src={`https://www.youtube.com/embed/${videoId}`}
          frameBorder="0"
          allowFullScreen
          title="LeBron Highlight"
        ></iframe>
      ) : (
        <p>Loading video...</p>
      )}
    </div>
  );
}

export default HighlightVid;
