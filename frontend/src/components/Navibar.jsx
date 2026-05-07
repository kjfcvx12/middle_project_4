import { Link } from "react-router-dom";
import { Warehouse, MapPin, Dumbbell, ClipboardList, MessageSquare, User } from "lucide-react";
import "../css/NaviBar.css"

const NaviBar = () => {
  return (
    <nav className="bottom-nav">
      <div className="nav-container">
        <Link className="nav-item" title="홈" to="/"><Warehouse size={24} /><span>홈</span></Link>
        <Link className="nav-item" title="헬스장" to="/gym"><MapPin size={24} /><span>헬스장</span></Link>
        <Link className="nav-item" title="루틴" to="/routine"><Dumbbell size={24} /><span>루틴</span></Link>
        <Link className="nav-item" title="기록" to="/logs"><ClipboardList size={24} /><span>기록</span></Link>
        <Link className="nav-item" title="커뮤니티" to="/board"><MessageSquare size={24} /><span>커뮤니티</span></Link>
        <Link className="nav-item" title="프로필" to="/profile"><User size={24} /><span>프로필</span></Link>
      </div>
    </nav>
  );
};

export default NaviBar;
