import React, { useEffect, useState } from 'react';
import { user_edit, user_profile } from './../../api/user';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import "./UserEdit.css"

const UserEdit = () => {
    const { user } = useAuth(); 

    const [editData, setEditData]=useState({pw: '', u_name: '', phone:'', info:'' })
    const [loading, setLoading] = useState(true);

    const navigate = useNavigate();

     useEffect(() => {
        const EditUserData = async () => {
            if (!user) return; 

            try {
                const profile= await user_profile(user);
                setEditData({pw: '', u_name: profile.u_name, phone: profile.phone, info:profile.info });
            } catch (error) {
                console.error("사용자 정보를 불러오는데 실패했습니다.", error);
            } finally {
                setLoading(false);
            }
        };
    
        EditUserData();
      }, []);


    

    const handleChange = (e) => {
        const { name, value} = e.target;

        setEditData({ ...editData, [name]: value });

    };


    // 로그인 처리
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (confirm("정말 수정하시겠습니까?")) {
            const result = await user_edit(editData);

            if (result.status==200) {
                alert('정보가 수정되었습니다.');
                setEditData({pw: '', u_name: '', phone:'', info:'' });
                navigate('/profile');
            } else {
                alert("정보 수정에 실패했습니다.");
            }
        }
    };



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
                        required
                    />
                    <input
                        name="u_name"
                        type="text"
                        placeholder="이름"
                        value={editData.u_name || ''}
                        onChange={handleChange}
                        required
                    />
                    <input
                        name="phone"
                        type="text"
                        placeholder="전화번호"
                        value={editData.phone || ''}
                        onChange={handleChange}
                        required
                    />
                    <textarea
                        name="info"
                        placeholder="자기소개"
                        value={editData.info || ''}
                        onChange={handleChange}
                        rows={5}
                        required
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