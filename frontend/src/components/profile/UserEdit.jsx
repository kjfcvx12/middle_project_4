import React, { useEffect, useState } from 'react';
import { user_edit, user_profile } from './../../api/user';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import "./UserEdit.css"

const UserEdit = () => {
    const { user } = useAuth(); 

    const [editData, setEditData]=useState({})
    const [loading, setLoading] = useState(true);

    const navigate = useNavigate();

     useEffect(() => {
        if (!user) {
            navigate('/login');
            return;
        }

        const EditUserData = async () => {
            if (!user) return; 

            try {
                const profile= await user_profile(user);
                const u_data=profile.data

                setEditData({u_id:u_data.u_id, pw: '', u_name: u_data.u_name, phone: u_data.phone, info:u_data.info });
            } catch (error) {
                console.error("사용자 정보를 불러오는데 실패했습니다.", error);
            } finally {
                setLoading(false);
            }
        };
    
        EditUserData();
      }, [user, navigate]);


    

    const handleChange = (e) => {
        const { name, value} = e.target;

        setEditData(i => ({ ...i, [name]: value }));

    };


    // 로그인 처리
    const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (window.confirm("정말 수정하시겠습니까?")) {
        const dataToSend = { ...editData };

        if (!dataToSend.pw || dataToSend.pw.trim() === "") {
            delete dataToSend.pw;
        }

        try {
            const result = await user_edit(dataToSend);

            if (result.status === 200) {
                alert('정보가 수정되었습니다.');
                navigate('/profile');
            } else {
                alert("정보 수정에 실패했습니다.");
            }
        } catch (error) {
            console.error("수정 중 오류 발생:", error);
            alert("서버와 통신 중 오류가 발생했습니다.");
        }
    }
};

    if (loading) return <div className="loading">로딩 중...</div>;


    return (
        <div className="user-edit-container">
            <h1>내 정보 수정</h1>

            <div>
                
                <form onSubmit={handleSubmit} className="user-edit-form">
                    <input
                        name="pw"
                        type="password"
                        placeholder="비밀번호"
                        value={editData.pw || ''}
                        onChange={handleChange}
                    />
                    <input
                        name="u_name"
                        type="text"
                        placeholder="이름"
                        value={editData.u_name || ''}
                        onChange={handleChange}
                    />
                    <input
                        name="phone"
                        type="text"
                        placeholder="전화번호"
                        value={editData.phone || ''}
                        onChange={handleChange}
                    />
                    <textarea
                        name="info"
                        placeholder="자기소개"
                        value={editData.info || ''}
                        onChange={handleChange}
                        rows={5}
                    />
                    <button type="submit">정보수정</button>
                    <Link to={"/profile"} className="cancel-link">
                        <button type="button" className="cancel-button">취소</button>
                    </Link>
                </form>
            </div>
        </div>
    );
};


export default UserEdit;