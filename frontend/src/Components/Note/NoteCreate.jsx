import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { user_email_get_id } from '../../api/user';
import { note_create } from '../../api/notes';

const NoteCreate = () => {
    const location = useLocation();
    const locData = location.state ||{};
    const navigate = useNavigate();
    const { userData } = useAuth();
    

    const [noteData, setNoteData] = useState({
        email: "",
        title: "",
        content: ""
    });

    const [loading, setLoading] = useState(false);

    // 입력값 변경 핸들러
    const handleChange = (e) => {
        const { name, value } = e.target;
        setNoteData({ ...noteData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (loading) return;
            setLoading(true);

    try {
        let currentReceId = 0;

        if (!locData.type && noteData.email) {
            

            const receId = await user_email_get_id(noteData.email);

            

            if (!receId) {
                alert("존재하지 않는 사용자 이메일입니다.");
                setLoading(false);
                return;
            }

            currentReceId=receId.u_id;

        } else if (locData.type == 'admin') {
            currentReceId = 1;
        }


        const payload = { 
            rece_id: Number(currentReceId),
            title: noteData.title,
            content: noteData.content 
        };
        
        console.log(payload)
        const result = await note_create(payload);

        if (result.status === 200 || result.status === 201) {
            alert(result.data);
            navigate('/note')
        } else {
            const errorMsg = error.result?.data?.detail || "쪽지 전송에 실패했습니다.";
            alert(errorMsg);
        }

        } catch (error) {
            console.error("전송 오류:", error);
            alert("서버 통신 중 오류가 발생했습니다.");
        } finally {
            setLoading(false);
        }
    };

    

    return (
        <div>
            <div>
                <h2>{locData?.title || '쪽지 작성'}</h2>
            </div>
            <form onSubmit={handleSubmit}>
                {locData.type? (<div>문의 내용</div>) :
                (<div>
                    <label htmlFor="email">받는 사람:</label>
                    <input type="email" 
                            id="email" 
                            name="email"
                            value={noteData.email} 
                            onChange={handleChange} 
                            required placeholder="Email을 입력하세요"/>
                </div>)}
                <label htmlFor="title">제목:</label>
                <input type="text" 
                       id="title" 
                       name="title"
                       value={noteData.title} 
                       onChange={handleChange} 
                       required placeholder="제목을 입력하세요"/>

                <label htmlFor="content">내용:</label>
                <textarea id="content" 
                          name="content"
                          value={noteData.content} 
                          rows="10" 
                          onChange={handleChange} 
                          required placeholder="내용을 입력하세요">
                        
                </textarea>

                <button type="submit" disabled={loading}>
                    {loading ? "전송 중..." : "전송"}
                </button>
                <button type="button" onClick={() => navigate(-1)}>취소</button>
            </form>
            
            
        </div>
    );
};

export default NoteCreate;