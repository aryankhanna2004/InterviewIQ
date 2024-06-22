import React, { useState } from 'react';
import axios from 'axios';

const Chat = () => {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Sending message:', message); // Debug log
    try {
      const res = await axios.post('/api/chat', { message });
      console.log('Received response:', res.data.response); // Debug log
      setResponse(res.data.response);
    } catch (error) {
      console.error('Error fetching the chat completion:', error);
      if (error.response) {
        console.log('Error response:', error.response);
      }
      setResponse('Error fetching the chat completion.');
    }
  };

  return (
    <div>
      <h1>Chat with LLM</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter your message"
        />
        <button type="submit">Send</button>
      </form>
      {response && (
        <div>
          <h2>Response:</h2>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default Chat;
