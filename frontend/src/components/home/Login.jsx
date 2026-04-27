import React, { useState } from 'react';
import { useAuth } from '../AuthContext';


const Login = () => {
    const { isLoggedIn, setIsLoggedIn, logout } = useAuth();

    const [isOpen, setIsOpen] = useState(true);
    const [loginData, setLoginData] = useState({ email: '', pw: '' });

    // 입력값 변경 핸들러
    const handleChange = (e) => {
        const { name, value } = e.target;
        setLoginData({ ...loginData, [name]: value });
    };

    // 로그인 처리
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("로그인 시도:", loginData.email);
        alert(`${loginData.e}님 환영합니다!`);
        setIsLoggedIn(true)
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
                            onChange={handleChange}
                            required
                        />
                        <input
                            name="pw"
                            type="pw"
                            placeholder="비밀번호"
                            onChange={handleChange}
                            required
                        />
                        <input type="checkbox" id="autologin" name="autologin" value="autologin"/>
                            <label for="autologin">로그인 상태 유지</label>
                        
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
                            onChange={handleChange}
                            required
                        />
                        <input
                            name="pw"
                            type="pw"
                            placeholder="비밀번호"
                            onChange={handleChange}
                            required
                        />
                        <input
                            name="u_name"
                            type="text"
                            placeholder="이름"
                            onChange={handleChange}
                            required
                        />
                        <input
                            name="phone"
                            type="text"
                            placeholder="전화번호"
                            onChange={handleChange}
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


