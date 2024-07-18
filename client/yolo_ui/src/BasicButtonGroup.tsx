import React from 'react';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';

export default function BasicButtonGroup() {
  return (
    <ButtonGroup variant="contained" aria-label="Basic button group">
      <Button onClick={handleCaptureOneImage}>Capture One Image</Button>
      <Button onClick={handleKeepCapturing}>Keep Capturing</Button>
      <Button onClick={handleStart}>Start</Button>
      <Button onClick={handleStop}>Stop</Button>
    </ButtonGroup>
  );
}

function handleCaptureOneImage() {
  fetch('http://localhost:5000/api/start')
    .then(response => {
      if (response.ok) {
        return response.json(); // Parse the response data as JSON
      } else {
        throw new Error('API request failed');
      }
    })

    .then(data => {
      // Process the response data here
      console.log(data);
    })

    .catch(error => {
      // Handle any errors here
      console.error(error);
    });
}

function handleKeepCapturing() {
  fetch('http://localhost:5000/api/stop')
    .then(response => {
      if (response.ok) {
        return response.json(); // Parse the response data as JSON
      } else {
        throw new Error('API request failed');
      }
    })

    .then(data => {
      // Process the response data here
      console.log(data);
    })

    .catch(error => {
      // Handle any errors here
      console.error(error);
    });
}


function handleStart() {
  //Send request to Flask server
  fetch('http://localhost:5000/api/start')
    .then(response => response.text())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
};

function handleStop() {
  //Send request to Flask server
  fetch('http://localhost:5000/api/stop')
    .then(response => response.text())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
};
