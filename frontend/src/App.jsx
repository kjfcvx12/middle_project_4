import React from 'react';
import { Link } from "react-router-dom";

const App = () => {
  return (
    <div>
      <Link><button>로그인</button></Link>
      <Link><button>회원가입</button></Link>
    </div>
  );
};

export default App;