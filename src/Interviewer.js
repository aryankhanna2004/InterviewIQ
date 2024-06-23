import React from 'react';
import './Interviewer.css';

function Interviewer() {
  return (
    <div className="container">
      <div className="main-content">
        <div className="left-panel">
          <div className="top-message">
            Thank you everyone for joining the design critique meeting. I want everyone's opinion, so please don't...
          </div>
          <div className="controls">
            <div className="control-button"></div>
            <div className="control-button"></div>
            <div className="control-button red-button"></div>
            <div className="control-button"></div>
            <div className="control-button"></div>
          </div>
        </div>
        <div className="right-panel">
          <div className="message">Looking away...</div>
          <div className="message">Speak more stern...</div>
          <div className="message">Nice answer!</div>
        </div>
      </div>
      <button className="new-button1">New</button>
      <button className="new-button2">Try Again</button>
      <div className="suggestions-container">
        <div className="percentage">91%</div>
        <h2 className="suggestions-title">Suggestions to Improve</h2>
        <div className="suggestions-content">
          <div className="strengths">Strengths</div>
          <div className="weakness">Weakness</div>
        </div>
        <div className="what-you-could-have-said">What you could have said</div>
      </div>
    </div>
  );
}

export default Interviewer;