import React, { useState } from 'react';
import { useAuth } from '../AuthContext';


const Login = () => {
    const { login, logout, signup } = useAuth();

    const [isOpen, setIsOpen] = useState(true);
    const [loginData, setLoginData] = useState({email: '', pw: '' });
    const [signupData, setSignupData] = useState({email: '', pw: '', u_name: '', phone:'' })

    // 입력값 변경 핸들러
    const handleChangeLogin = (e) => {
        const { name, value } = e.target;
        setLoginData({ ...loginData, [name]: value });
    };


    const handleChangeSignup = (e) => {
        const { name, value } = e.target;
        setSignupData({ ...signupData, [name]: value });
    };


    // 로그인 처리
    const handleSubmit = (e) => {
    e.preventDefault();
    
    if (isOpen) {
        // 로그인 로직
        console.log("로그인 시도:", loginData.email);
        alert(`${loginData.email}님 환영합니다!`);
        login(loginData);
    } else {
        // 회원가입 로직
        console.log("회원가입 시도:", signupData.email);
        alert("회원가입이 완료되었습니다.");
        signup(signupData)
    }
};

    return (
        <div style={{ padding: '50px', textAlign: 'center' }}>

        {isOpen && (
            <div>
                <div>
                    <h2>로그인</h2>
                    <form onSubmit={handleSubmit} style={formStyle}>
                        <input
                            name="email"
                            placeholder="email"
                            value={loginData.email}
                            onChange={handleChangeLogin}
                            required
                        />
                        <input
                            name="pw"
                            type="password"
                            placeholder="비밀번호"
                            value={loginData.pw}
                            onChange={handleChangeLogin}
                            required
                        />
                        <input type="checkbox" id="autologin" name="autologin" value="autologin"/>
                            <label htmlFor="autologin">로그인 상태 유지</label>
                        
                         {/* Silent Refresh 사용법 */}
                        <button type="submit">로그인</button>
                    </form>
                    <button>
                        아이디 찾기
                    </button>
                    <button>
                        비밀번호 찾기
                    </button>
                    <button onClick={() => setIsOpen(false)}>
                        회원가입
                    </button>
                </div>
            </div>
        )}




        {!isOpen && (
            <div>
                <div>
                    <h2>회원가입</h2>
                    <form onSubmit={handleSubmit} style={formStyle}>
                        <input
                            name="email"
                            placeholder="email"
                            onChange={handleChangeSignup}
                            required
                        />
                        <input
                            name="pw"
                            type="password"
                            placeholder="비밀번호"
                            onChange={handleChangeSignup}
                            required
                        />
                        <input
                            name="u_name"
                            type="text"
                            placeholder="이름"
                            onChange={handleChangeSignup}
                            required
                        />
                        <input
                            name="phone"
                            type="text"
                            placeholder="전화번호"
                            onChange={handleChangeSignup}
                            required
                        />
                        <button type="submit">회원가입</button>
                    </form>
                    <button onClick={() => setIsOpen(true)}>
                        로그인
                    </button>
                </div>
            </div>
        )}
        </div>
    );
    }


    const formStyle = { display: 'flex', flexDirection: 'column', gap: '10px' };

export default Login;


