import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Link } from 'react-router-dom';

import NaviBar from './components/NaviBar';
import Home from './components/home/Home';
import Gym from './components/gym/Gym';
import Routine from './components/routine/Routine';
import Log from './components/log/Log';
import Board from './components/board/Board';
import Profile from './components/profile/Profile';

const App = () => {

  const navStyle = {
        position: 'fixed',
        bottom: 0,
        left: 0,
        width: '100%',
        height: '60px',
        backgroundColor: '#fff',
        borderTop: '1px solid #ccc',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center'
    };

  

  return (
    <Router>
      <div>
        <p>home</p>

        <section>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/gym" element={<Gym />} />
            <Route path="/routine" element={<Routine />} /> 
            <Route path="/log" element={<Log />} />
            <Route path="/board" element={<Board />} />
            <Route path='/profile' element={<Profile/>}/>
          </Routes>
        </section>

        <footer className='bottom-nav' style={navStyle}>
          <NaviBar />
        </footer>
      </div>
    </Router>
  );
};

export default App;