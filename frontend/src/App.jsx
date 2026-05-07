import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import NaviBar from './components/NaviBar';
import Home from './components/home/Home';
import Login from './components/home/Login';
import Gym from './components/gym/Gym';
import Routines_page from './components/routine/routines_page';
import Log from './components/log/Log';
import Board from './components/board/Board';
import Profile from './components/profile/Profile';
import { useAuth } from './components/AuthContext';
import MachineList from './components/routine/machine/machine_list';
import MachineDetail from './components/routine/machine/machine_detail';
import MachineCreate from "./components/routine/machine/machine_create";
import Routine_details from './components/routine/Routine_details';
import routines_page from './components/routine/routines_page';
import NoteCreate from './components/Note/NoteCreate';
import NoteDetail from './components/Note/NoteDetail';
import NoteBox from './components/Note/NoteBox';
import UserEdit from './components/profile/UserEdit';
import GymCreate from './Components/gym/GymCreate'
import GymEdit from './Components/gym/GymEdit'
import Routine from './Components/routine/routines_page'
import PartCreate from './components/Part/PartCreate'


const ProtectedRoute = ({ isLoggedIn }) => {
  return isLoggedIn ? <Outlet /> : <Navigate to="/login" replace />;
};

const App = () => {
  const { isLoggedIn } = useAuth();

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
          <Routes>{(!isLoggedIn &&
            <Route path="/" element={<Login />} />)}

            <Route element={<ProtectedRoute isLoggedIn={isLoggedIn} />}>
              <Route path="/" element={<Home />} />
              <Route path="/gym" element={<Gym />} />
              <Route path="/routine" element={<Routines_page />} />
              <Route path="/routine/:r_id" element={<Routine_details />} /> 
              <Route path="/logs" element={<Log />} />
              <Route path="/gym/create" element={<GymCreate />} />
              <Route path="/gym/edit/:id" element={<GymEdit />} />
              <Route path="/log" element={<Log />} />
              <Route path="/board" element={<Board />} />
              <Route path="/profile" element={<Profile />} />
              {/* 머신 추가 */}
              <Route path="/gyms/:g_id/machines" element={<MachineList />} />
              <Route path="/gyms/:g_id/machines/create" element={<MachineCreate />} />
              <Route path="/gyms/:g_id/machines/:m_id" element={<MachineDetail />} />
              <Route path="/gyms/:g_id/machines/edit/:m_id" element={<MachineCreate />} />

              <Route path='/gym_machines/:g_id' element={<MachineList />} />
              <Route path="/profile/edit" element={<UserEdit />} />
              <Route path="/note/create" element={<NoteCreate />} />
              <Route path="/note/:n_id" element={<NoteDetail />} />
              <Route path="/note" element={<NoteBox />} />

              <Route path="/parts/create" element={<PartCreate/>}/>
              
              
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
