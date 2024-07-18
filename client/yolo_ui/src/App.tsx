import React from 'react';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import { styled } from '@mui/material/styles';
import WebsocketDisplay from './WebsocketDisplay';
import BasicButtonGroup from './BasicButtonGroup';
import { useState } from 'react';

const Item = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  textAlign: 'center',
  width: '300px',
  height: '300px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  color: theme.palette.text.secondary,
}));




function App() {
  // Variable Declare here
  const [start, setStart] = useState(false);

  const startProgram=() => {
    if (!start) {
      console.log('Program started!!');
      setStart(true);
    }
  };



  return (
    <>
      <Grid container spacing={5} justifyContent="center" alignItems="center">
        <Grid item xs={6}>
          <WebsocketDisplay />
        </Grid>
        <Grid item xs={6}>
          <Item>Right Grid</Item>
        </Grid>
      </Grid>
      <BasicButtonGroup />
    </>

  )
};

export default App;
