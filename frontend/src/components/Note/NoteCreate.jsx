import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { user_email_get_id, user_profile } from '../../api/user';
import { note_create } from '../../api/notes';

const NoteCreate = () => {
    const [searchParams] = useSearchParams();
    const u_id = searchParams.get("u_id");
    const email= searchParams.get("email");

    const location = useLocation();
    const locData = location.state ||{};
    const navigate = useNavigate();
    const { userData } = useAuth();
    

    const [noteData, setNoteData] = useState({
        email: email || "",
        title: locData.defaultTitle || "",
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

            if (locData.replyTo) {
                    currentReceId = locData.replyTo;
                    
                } 
                // 2. 관리자 문의인 경우
                else if (locData.type === 'admin') {
                    currentReceId = 1;
                } 
                // 3. 직접 이메일을 입력해서 보내는 경우
                else if (noteData.email) {
                    const receId = await user_email_get_id(noteData.email);
                    if (!receId) {
                        alert("존재하지 않는 사용자 이메일입니다.");
                        setLoading(false);
                        return;
                    }
                    currentReceId = receId.u_id;
                }

            if (!currentReceId) {
                alert("수신자 정보가 없습니다.");
                setLoading(false);
                return;
            }
            

            const payload = { 
                rece_id: Number(currentReceId),
                title: noteData.title,
                content: noteData.content 
            };
            
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
                <h2>{locData?.replyTo ? '답장 쓰기' : (locData?.title || '쪽지 작성')}</h2>
            </div>
            <form onSubmit={handleSubmit}>
                {!(locData.replyTo || locData.type) && (
                <div>
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
                       value={noteData.title || ""} 
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