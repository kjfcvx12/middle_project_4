import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { note_detail, note_rece_del, note_send_del } from '../../api/notes';
import { useAuth } from '../AuthContext';
import { user_profile } from '../../api/user';

const NoteDetail = () => {
    const { n_id } = useParams();
    const navigate = useNavigate();
    const { userData } = useAuth();
    
    const [note, setNote] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchNote = async () => {
            try {
                const result = await note_detail(n_id);
                if (result.status === 200 || result.success) {
                    setNote(result.data);

                } else {
                    alert("쪽지를 찾을 수 없습니다.");
                    navigate('/note');
                }
            } catch (error) {
                console.error("데이터 로드 오류:", error);
                navigate('/note');
            } finally {
                setLoading(false);
            }
        };
        fetchNote();
    }, [n_id, navigate]);

    const handleDelete = async () => {        
        try {
            if (confirm("정말 삭제하시겠습니까?")){
                let result;
                const isSender = userData.u_id === note.send_id;

                if (isSender) {
                    result = await note_send_del(n_id);
                } else {
                    result = await note_rece_del(n_id);
                }

                if (result.status === 200 || result.success) {
                    alert("삭제되었습니다.");
                    navigate('/note');
                }
            }
        } catch (error) {
            console.error("삭제 오류:", error);
            alert("삭제 중 오류가 발생했습니다.");
        }
    };

    if (loading) return <div>로딩 중...</div>;
    if (!note) return null;

    // 내가 받은 사람인지 확인
    const isReceiver = userData && userData.u_id === note.rece_id;

    return (
        <div>
            <h2>쪽지 상세 보기</h2>
            <div>
                <p>보낸 사람: {(note.send_id === 1 ? '관리자' : note.send_email)}</p> 
                <p>받는 사람: {(note.rece_id === 1 ? '관리자' : note.rece_email)}</p>
                <p>날짜: {new Date(note.n_date).toLocaleString()}</p>
                <h3>{note.title}</h3>
                <div>{note.content}</div>
            </div>

            <div>
                <button onClick={() => navigate('/note')}>목록</button>
                
                {isReceiver && (
                    <button onClick={() => navigate('/note/create', 
                    { state: { replyTo: note.send_id,
                    defaultTitle: note.send_id === 1 
                    ? `[재문의] ${note.title}` 
                    : `Re: ${note.title}`
                    } })}>
                        {note.send_id === 1 ? '재문의' : '답장'}
                    </button>
                )}
                
                <button onClick={handleDelete} style={{ color: 'red' }}>
                    삭제하기
                </button>
            </div>
        </div>
    );
};

export default NoteDetail;
