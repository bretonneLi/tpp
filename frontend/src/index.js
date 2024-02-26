import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Panda from './Panda';
import reportWebVitals from './reportWebVitals';
import Chatbot from './chatbot';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    {/* <Panda /> */}
<Chatbot />    
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
