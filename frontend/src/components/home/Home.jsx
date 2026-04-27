import React, { useState } from 'react';

const Home = () => {
    const [isOpen, setIsOpen] = useState(false);
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
        setIsOpen(false);
    };

    return (
        <div style={{ padding: '50px', textAlign: 'center' }}>
        <h1>main</h1>
        <button onClick={() => setIsOpen(true)} style={loginBtnStyle}>
            로그인
        </button>

        {isOpen && (
            <div style={overlayStyle}>
                <div style={modalStyle}>
                    <h2>Login</h2>
                    <form onSubmit={handleSubmit} style={formStyle}>
                        <input
                            name="email"
                            placeholder="email"
                            onChange={handleChange}
                            style={inputStyle}
                            required
                        />
                        <input
                            name="pw"
                            type="pw"
                            placeholder="비밀번호"
                            onChange={handleChange}
                            style={inputStyle}
                            required
                        />
                        <button type="submit" style={submitBtnStyle}>로그인</button>
                    </form>
                </div>
            </div>
        )}
        </div>
    );
    }

    const overlayStyle = {
    position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
    backgroundColor: 'rgba(0,0,0,0.6)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000
    };

    const modalStyle = {
    backgroundColor: '#fff', padding: '30px', borderRadius: '12px', width: '320px', textAlign: 'center'
    };

    const formStyle = { display: 'flex', flexDirection: 'column', gap: '10px' };

    const inputStyle = { padding: '12px', borderRadius: '5px', border: '1px solid #ddd' };

    const loginBtnStyle = { padding: '10px 20px', fontSize: '16px', cursor: 'pointer' };

    const submitBtnStyle = { 
    padding: '12px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' 
    };

    // const closeBtnStyle = { backgroundColor: 'transparent', border: 'none', color: '#888', cursor: 'pointer', marginTop: '10px' };


export default Home;