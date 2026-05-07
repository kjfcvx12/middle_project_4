import React, { useState } from 'react';
import { user_find_email } from './../../api/user';
import "./Login.css"

const Find = () => {
    const [isFindEmailOpen, setIsFindEmailOpen] = useState(false);
    const [findEmailData, setFindEmailData] = useState({ u_name: "", phone: "" });

    const handleFindEmailSubmit = async (e) => {
        e.preventDefault();
        try {
            const result = await user_find_email(findEmailData);
            if (result && result.data) {
                alert(`찾으시는 이메일은 ${result.data}입니다.`);
                setIsFindEmailOpen(false);
            } else {
                alert("일치하는 정보가 없습니다.");
            }
        } catch (error) {
            alert("오류가 발생했습니다.");
        }
    };

    return (
        <>
            <button className="switch-btn" onClick={() => setIsFindEmailOpen(true)}>아이디 찾기</button>

            {isFindEmailOpen && (

            <div style={{
                position: 'fixed',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                backgroundColor: 'rgba(0, 0, 0, 0.5)',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                zIndex: 9999
            }}>

                <div style={{
                    backgroundColor: 'gray',
                    padding: '20px',
                    borderRadius: '8px'
                }}>
                        <h3>아이디 찾기</h3>
                        <form onSubmit={handleFindEmailSubmit}>
                            <input 
                                type="text"
                                placeholder="이름" 
                                value={findEmailData.u_name}
                                onChange={(e) => setFindEmailData({...findEmailData, u_name: e.target.value})} 
                                required 
                            /><br/>
                            <input 
                                type="text"
                                placeholder="전화번호" 
                                value={findEmailData.phone}
                                onChange={(e) => setFindEmailData({...findEmailData, phone: e.target.value})} 
                                required 
                            />
                            <div>
                                <button type="submit" className="submit-btn">확인</button>
                                <button type="button" className="submit-btn" onClick={() => setIsFindEmailOpen(false)}>취소</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </>
    );
};


export default Find;
