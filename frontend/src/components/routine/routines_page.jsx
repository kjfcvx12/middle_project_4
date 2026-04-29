import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { routines_read,routines_create,routines_delete } from '../../api/routines';


const routines_page = () => {

    const nav = useNavigate();
    const [list, setList] = useState([]);
    const [name, setName] = useState('');

    // 최초 랜더링 시 루틴 가져오기
    useEffect(()=>{
        fetch_routines();
    },[]);

    // 루틴 불러오기
    const fetch_routines =  async() => {
        try{
            const response = await routines_read();
            setList(response.data.data);
        }catch (err){
            console.error(err);
        }
    };

    // 루틴 생성
    const handle_create = async()=>{
        if(!name) return ;
    
        try{
            await routines_create({r_name : name});

            setName('');
            fetch_routines();
        }catch(err){
            console.error(err);
        }
    };

    // 루틴 삭제
    const handle_delete = async (r_id) =>{
        try {
            await routines_delete(r_id);
            fetch_routines();
        } catch(err){
            console.error(err);
        }
    };


  return (
    <div>
        <h1>루틴 관리</h1>

        {/* 루틴 생성 */}
        <div>
            <input value={name} onChange={(e)=> setName(e.target.value)}
            placeholder='루틴 이름'  />

            <button onClick={handle_create}>루틴 생성</button>
        </div>

        {/* 루틴 리스트 띄우기 */}
        {
            list.map((routines)=>(
                <div key={routines.r_id}>
                    {/* 루틴 클릭하면 루틴 상세 */}
                    <div onClick={()=> nav(`/routine/${routines.r_id}`)}>
                        <h3>{routines.r_name}</h3>
                        <p>{routines.p_name}</p>
                    </div>
                    {/* 삭제 버튼 */}
                    <button onClick={()=> handle_delete(routines.r_id)} >삭제</button>
                </div>
            ))
        }


    </div>
  )
}

export default routines_page