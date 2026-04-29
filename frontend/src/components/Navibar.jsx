import { Link, useNavigate } from "react-router-dom";

const NaviBar = () => {
  const navigator = useNavigate();

  return (
    <nav>
      <table>
        <tbody>
          <tr>
            <td>
              <Link to="/">home</Link>
            </td>
            <td>
              <Link to="/gym">헬스장</Link>
            </td>
            <td>
              <Link to="/routine">루틴</Link>
            </td>
            <td>
              <Link to="/log">기록</Link>
            </td>
            <td>
              <Link to="/board">커뮤니티</Link>
            </td>
            <td>
              <Link to="/profile">프로필</Link>
            </td>
          </tr>
        </tbody>
      </table>
    </nav>
  );
};

export default NaviBar;
