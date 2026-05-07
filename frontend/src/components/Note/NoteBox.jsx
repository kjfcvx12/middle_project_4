import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { note_inbox, note_outbox } from '../../api/notes';
import './NoteBox.css';

const NoteBox = () => {
    const navigate = useNavigate();
    const { userData } = useAuth();
    const location=useLocation();
    
    const [tab, setTab] = useState(location.state?.activeTab || 'inbox');
    const [notes, setNotes] = useState([]);
    const [loading, setLoading] = useState(true);

    


    useEffect(() => {
        fetchNotes();
    }, [tab]);

    const fetchNotes = async () => {
        setLoading(true);
        try {
            const result = tab === 'inbox' 
                ? await note_inbox()
                : await note_outbox()
                
            if (result.status==200 || result.status==201) {
                setNotes(result.data);
            }
        } catch (error) {
            console.error("목록 로드 오류:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="note-container">
            <div className="note-header">
                <h2>{tab === 'inbox' ? '받은 쪽지함' : '보낸 쪽지함'}</h2>
                
            </div>


            <div className="tab-group">
                <button className={`tab-btn ${tab === 'inbox' ? 'active' : ''}`}  
                        onClick={() => setTab('inbox')}>
                        받은 쪽지
                </button>
                <button className={`tab-btn ${tab === 'outbox' ? 'active' : ''}`}
                        onClick={() => setTab('outbox')}>
                        보낸 쪽지
                </button>

                <button className="btn-create" 
                        onClick={() => navigate('/note/create')}>
                    쪽지 쓰기
                </button>  
            </div>

            

            {loading ? (
                <div className="loading">로딩 중...</div>
            ) : (
                <table className="note-table">
                    <thead>
                        <tr>
                            <th>{tab === 'inbox' ? ' 보낸 사람' : '받는 사람'}</th>
                            <th>제목</th>
                            <th>날짜</th>
                        </tr>
                    </thead>
                    <tbody>
                        {notes.length > 0 ? (
                            notes.map((note) => (
                                <tr key={note.n_id} 
                                    onClick={() => navigate(`/note/${note.n_id}`, { state: { fromTab: tab } })} >
                                    <td style={{ width: '30%', textAlign: 'left', paddingLeft: '20px' }}>
                                        {tab === 'inbox' 
                                        ? (note.send_id === 1 ? '관리자' : note.send_email) 
                                        : (note.rece_id === 1 ? '관리자' : note.rece_email) }
                                    </td>
                                    <td style={{ width: '50%', textAlign: 'left' }}>
                                        {note.title}
                                    </td>
                                    <td style={{ width: '20%', textAlign: 'center', color: '#888' }}>
                                        {new Date(note.n_date).toLocaleDateString()}
                                    </td>
                                </tr>))
                        ) : (
                            <tr>
                                <td colSpan="3" className="no-data">
                                    쪽지가 없습니다.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default NoteBox;