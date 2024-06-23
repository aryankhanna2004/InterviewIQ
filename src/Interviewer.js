import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ReactPlayer from 'react-player';
import './Interviewer.css';

function Interviewer() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState({
    rating: null,
    strengths: [],
    weaknesses: [],
    suggestions_for_improvement: [],
    stronger_response: ''
  });
  const [emotions, setEmotions] = useState([]);
  const [currentEmotions, setCurrentEmotions] = useState([]);
  const playerRef = useRef(null);

  const videoUrl = 'https://jbdehsbckejkbdkhwx.s3.amazonaws.com/IMG_4648.mp4'; // Replace with your actual S3 video URL

  useEffect(() => {
    // Fetch the emotion data from the backend
    setMessage('Tell me about a time when you had to work with a difficult person. How did you handle the situation?');
    axios.get('/api/emotions')
      .then(res => {
        setEmotions(res.data);
      })
      .catch(error => {
        console.error('Error fetching emotions:', error);
      });
  }, []);

  const handleButtonClick = async () => {
    if (!message.trim()) {
      console.error('Message is empty. Please provide a message.');
      setResponse({
        rating: null,
        strengths: [],
        weaknesses: [],
        suggestions_for_improvement: [],
        stronger_response: 'Message is empty. Please provide a message.'
      });
      return;
    }

    try {
      const res = await axios.post('/api/chat', { message }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      setResponse(JSON.parse(res.data.response));
    } catch (error) {
      console.error('Error fetching response:', error);
      if (error.response) {
        console.log('Error response:', error.response);
      }
      setResponse({
        rating: null,
        strengths: [],
        weaknesses: [],
        suggestions_for_improvement: [],
        stronger_response: 'Error fetching the response from the API.'
      });
    }
  };

  const handleProgress = (state) => {
    const currentTime = state.playedSeconds;

    // Find the current emotions based on the video time
    const current = emotions.find(
      (emotion) => currentTime >= emotion.BeginTime && currentTime <= emotion.EndTime
    );

    if (current) {
      setCurrentEmotions(current.Top_3_Labels);
    } else {
      setCurrentEmotions([]);
    }
  };

  return (
    <div className="container">
      <div className="main-content">
        <div className="left-panel">
          <div className="top-message">
            QUESTION: Tell me about a time when you had to work with a difficult person. How did you handle the situation?
          </div>
          <div className="video-player">
            <ReactPlayer
              ref={playerRef}
              url={videoUrl}
              controls={true}
              onProgress={handleProgress}
            />
          </div>
          <div className="controls">
            <div className="control-button"></div>
            <div className="control-button"></div>
            <div className="control-button red-button" onClick={handleButtonClick}></div>
            <div className="control-button"></div>
            <div className="control-button"></div>
          </div>
        </div>
        <div className="right-panel">
          <h3>Current Emotions:</h3>
          <ul>
            {currentEmotions.length > 0 ? (
              currentEmotions.map((emotion, index) => (
                <li key={index}>{emotion}</li>
              ))
            ) : (
              <li>No emotions detected</li>
            )}
          </ul>
        </div>
      </div>
      <button className="new-button1">New</button>
      <button className="new-button2">Try Again</button>
      <div className="suggestions-container">
        <div className="percentage">{response.rating !== null ? `${response.rating}%` : 'N/A'}</div>
        <h2 className="suggestions-title">Suggestions to Improve</h2>
        <div className="suggestions-content">
          <div className="strengths">
            <h3>Strengths</h3>
            <ul>
              {response.strengths.length > 0 ? (
                response.strengths.map((strength, index) => (
                  <li key={index}>{strength}</li>
                ))
              ) : (
                <li>No strengths provided</li>
              )}
            </ul>
          </div>
          <div className="weakness">
            <h3>Weaknesses</h3>
            <ul>
              {response.weaknesses.length > 0 ? (
                response.weaknesses.map((weakness, index) => (
                  <li key={index}>{weakness}</li>
                ))
              ) : (
                <li>No weaknesses provided</li>
              )}
            </ul>
          </div>
          <div className="improvement">
            <h3>Suggestions for Improvement</h3>
            <ul>
              {response.suggestions_for_improvement.length > 0 ? (
                response.suggestions_for_improvement.map((suggestion, index) => (
                  <li key={index}>{suggestion}</li>
                ))
              ) : (
                <li>No suggestions provided</li>
              )}
            </ul>
          </div>
          <div className="stronger-response">
            <h3>Stronger Response</h3>
            <p>{response.stronger_response || 'No stronger response provided'}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Interviewer;
