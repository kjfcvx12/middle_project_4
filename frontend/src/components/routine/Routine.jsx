import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { routines_create, routines_read } from '../../api/routines';

const Routine = () => {
    const nav = useNavigate();

    const [list,setList] = useState([]);
    const [loading, setLoading]=useState([]);
    

    useEffect(() =>{
        fetch_routines();
    },[]);

    const fetch_routines = async ()=>{
        try{
            const response = await routines_read();

            console.log("루틴 읽기 응답", response.data);

            setList(response.data.data);
        } catch (err) {
            console.error("루틴 조회 실패", err);
        } finally{
            setLoading(false)
        }
    };

    if (loading) return <div>로딩중...</div>;
    
    return (
        <div>
            <h1>루틴 관리</h1>
            {list.map((r) => (
                <div
                key={r.r_id}
                onClick={()=> nav(`/routine/${r.r_id}`)}
                >
                    <h3>{r.r_name}</h3>
                    <p>부위 : {r.p_name}</p>
                </div>

            )
        )}
            
        </div>
    );
};

export default Routine;