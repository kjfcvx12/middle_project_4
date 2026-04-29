import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import NaviBar from './components/NaviBar';
import Home from './components/home/Home';
import Login from './components/home/Login';
import Gym from './components/gym/Gym';
import Routine from './components/routine/Routine';
import Log from './components/log/Log';
import Board from './components/board/Board';
import Profile from './components/profile/Profile';
import { useAuth } from './components/AuthContext';
import MachineList from './components/routine/machine/machine_list';
import MachineDetail from './components/routine/machine/machine_detail';




const ProtectedRoute = ({ isLoggedIn }) => {
  return isLoggedIn ? <Outlet /> : <Navigate to="/login" replace />;
};

const App = () => {
  const { isLoggedIn} = useAuth();

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
    alignItems: 'center',
    zIndex: 1000
  };

  return (
    <Router>
      <div style={{ paddingBottom: '60px' }}>
        <section>
          <Routes>{(!isLoggedIn&&
            <Route path="/" element={<Login />} />)}
            
            <Route element={<ProtectedRoute isLoggedIn={isLoggedIn} />}>
              <Route path="/" element={<Home />} />
              <Route path="/gym" element={<Gym />} />
              <Route path="/routine" element={<Routine />} />
              <Route path="/log" element={<Log />} />
              <Route path="/board" element={<Board />} />
              <Route path="/profile" element={<Profile />} />
              {/* 머신 추가 */}
              <Route path="/machines" element={<MachineList />} />
              <Route path="/machines/:m_id" element={<MachineDetail />} />
            </Route>


            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </section>

        {isLoggedIn && (
          <footer className="bottom-nav" style={navStyle}>
            <NaviBar />
          </footer>
        )}
      </div>
    </Router>
  );
};

export default App;
