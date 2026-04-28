import { Link, useNavigate } from "react-router-dom";

const NaviBar = () => {
  const navigator = useNavigate();

  return (
    <nav>
      <table>
        <tr>
          <Link to="/">
            <td>home</td>
          </Link>
          <Link to="/gym">
            <td>헬스장</td>
          </Link>
          <Link to="/routine">
            <td>루틴</td>
          </Link>
          <Link to="/log">
            <td>기록</td>
          </Link>
          <Link to="/board">
            <td>커뮤니티</td>
          </Link>
          <Link to="/profile">
            <td>프로필</td>
          </Link>
        </tr>
      </table>
    </nav>
  );
};

export default NaviBar;
