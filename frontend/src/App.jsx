import { Route, BrowserRouter as Router, Routes } from "react-router-dom";

import NaviBar from "./components/NaviBar";
import Board from "./components/board/Board";
import Gym from "./components/gym/Gym";
import Home from "./components/home/Home";
import Log from "./components/log/Log";
import Profile from "./components/profile/Profile";
import Routine from "./components/routine/Routine";

const App = () => {
  const navStyle = {
    position: "fixed",
    bottom: 0,
    left: 0,
    width: "100%",
    height: "60px",
    backgroundColor: "#fff",
    borderTop: "1px solid #ccc",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  };

  return (
    <Router>
      <div>
        <section>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/gym" element={<Gym />} />
            <Route path="/routine" element={<Routine />} />
            <Route path="/log" element={<Log />} />
            <Route path="/board" element={<Board />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </section>

        <footer className="bottom-nav" style={navStyle}>
          <NaviBar />
        </footer>
      </div>
    </Router>
  );
};

export default App;
