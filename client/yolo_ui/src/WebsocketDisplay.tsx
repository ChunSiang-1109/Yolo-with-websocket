import React from 'react';
import { useState, useEffect, useRef, RefObject } from 'react';

export default function WebsocketDisplay({image}: {image: RefObject<HTMLImageElement>}) {
  return (
    <React.Fragment>
      <img ref={image} alt="Webcam stream"  style={{ width: '100%', height: 'auto' }}/>
    </React.Fragment>);
}