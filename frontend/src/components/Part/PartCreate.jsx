import React, { useEffect, useState } from 'react';
import { createParts, deleteParts, getParts } from '../../api/parts';
import "./part.css"

const PartCreate = () => {
    const [partName, setPartName] = useState({p_name:''});
    const [loading, setLoading] = useState(false);
    const [partData, setPartData]=useState([]);

    const fetchParts = async () => {
        try {
            const response = await getParts();
            setPartData(Array.isArray(response.data.data) ? response.data.data : []);
        } catch (error) {
            console.error("데이터 로드 실패:", error);
        }
    };

    useEffect(() => {
        fetchParts();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setPartName({...partName, [name]: value});
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        if (loading) return;
            setLoading(true);
    
        try {                
            const result = await createParts(partName)
            alert("등록 성공!");
            setPartName({ p_name: '' });
            fetchParts();
        } catch (error) {
            console.error("전송 오류:", error);
            alert("서버 통신 중 오류가 발생했습니다.");
        } finally {
            setLoading(false);
        }
    };


     const handleDelete = async (p_id) => {
        if (!window.confirm("정말 삭제하시겠습니까?")) return;
        
        try {
            await deleteParts(p_id);
            alert("삭제되었습니다.");
            fetchParts();
        } catch (error) {
            console.error("삭제 오류:", error);
            alert("삭제에 실패했습니다.");
        }
    };

    return (
        <div className="part-container">
            <form className="part-form" onSubmit={handleSubmit}>
            <input type='text' 
            id='p_name'
            name='p_name' 
            className="part-input"
            value={partName.p_name}
            onChange={handleChange}
            required placeholder="부위를 입력하세요" />

            <button type='submit' className="submit-btn">등록</button>
            </form>

            <hr />
            <div className="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>부위 명칭</th>
                            <th style={{ textAlign: 'right' }}>관리</th>
                        </tr>
                    </thead>
                    <tbody>
                        {partData.map((part) => (
                            <tr key={part.p_id}>
                                <td>{part.p_name}</td>
                                <td style={{ textAlign: 'right' }}>
                                    <button className="delete-btn"
                                            onClick={() => handleDelete(part.p_id)}>
                                        삭제
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default PartCreate;