import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { note_detail, note_rece_del, note_send_del } from '../../api/notes';
import { useAuth } from '../AuthContext';

const NoteDetail = () => {
    const { noteId } = useParams();
    const navigate = useNavigate();
    const { userData } = useAuth();
    
    const [note, setNote] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchNote = async () => {
            try {
                const result = await note_detail(noteId);
                if (result.success) {
                    setNote(result.data);
                } else {
                    alert("쪽지를 찾을 수 없습니다.");
                    navigate('/note');
                }
            } catch (error) {
                console.error("데이터 로드 오류:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchNote();
    }, [noteId, navigate]);

    const handleDelete = async () => {
        if (!window.confirm("정말 삭제하시겠습니까?")) return;
        
        const result = await note_rece_del(noteId)
        if (result.success) {
            alert("삭제되었습니다.");
            navigate('/note');
        }
    };


    if (loading) return <div>로딩 중...</div>;
    if (!note) return null;

    return (
        <div>
            <h2>쪽지 상세 보기</h2>
            <div>
                <div>
                    <p><strong>보낸 사람:</strong> {note.sender_email}</p>
                    <p><strong>날짜:</strong> {new Date(note.created_at).toLocaleString()}</p>
                    <hr />
                    <h3>{note.title}</h3>
                </div>
                
                <div>
                    {note.content}
                </div>
            </div>

            <div>
                <button onClick={() => navigate('/note')}>목록으로</button>
            </div>
        </div>
    );
};

export default NoteDetail;
