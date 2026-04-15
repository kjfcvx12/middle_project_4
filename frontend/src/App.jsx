import React from 'react';
import { Link } from "react-router-dom";

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
    <div>
      <p>home</p>

      
      <nav className='bottom-nav' style={navStyle}>
        <table>
        <tr>
          <td>home</td>
          <td>헬스장</td>
          <td>루틴</td>
          <td>기록</td>
          <td>커뮤니티</td>
          <td>프로필</td>
        </tr>
      </table>
      </nav>
    </div>
  );
};

export default App;