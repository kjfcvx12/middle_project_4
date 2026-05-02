import React, { useEffect, useState } from 'react'
import { data, useNavigate } from 'react-router-dom';
import { routines_read,routines_create,routines_delete } from '../../api/routines';
import { getParts } from '../../api/parts';
import { routine_detail_create } from './../../api/routine_details';
import { machines_read } from './../../api/machines';

const Routines_page = () => {

    const nav = useNavigate();

    const [list, setList] = useState([]);
    const [name, setName] = useState('');

    const [parts, setParts] = useState([]);
    const [p_id, setP_id] = useState("");

    const [open, setOpen] = useState(false);

    const [details, setDetails] = useState([{
        m_id: "",
        step: 1,
        sets: "",
        reps: "",
        rest_time: "",
        weight:"",
    }])

    const [machines, setMachines] = useState([]);


    // 최초 랜더링 시 루틴 가져오기
    useEffect(()=>{
        fetch_routines();
        fetch_parts();
    },[]);

    // 루틴 불러오기
    const fetch_routines =  async() => {
        try{
            const response = await routines_read();
            setList(response.data.data);
        }catch (err){
            console.error(err.response?.data || err);
        }
    };
     // 운동부위 불러오기
    const fetch_parts = async () => {
        try {
            const response = await getParts();

            setParts(response.data.data || response.data);
        } catch (err) {
            console.error(err.response?.data || err);
        }
        };

    // 운동 추가
    const handle_add_detail = () =>{
        setDetails([
            ...details,{
                m_id: "",
                step: details.length + 1,
                sets: "",
                reps: "",
                rest_time: "",
                weight:"",
            }
        ])
    }

    const handle_detail_change = (index, field, value) =>{
        const newDetails = [...details];
        newDetails[index][field] = value;
        setDetails(newDetails);
    };

    // 루틴/디테일 생성
    const handle_create = async()=>{
        if(!name || !p_id){
            alert('루틴 이름과 부위를 설정하세요')
        } 
        return ;
    
        try{
            // 루틴 생성
            const response = await routines_create(
                {r_name : name,
                p_id: Number(p_id),
                }
            );

            const r_id = response.data.r_id;

            // 루틴 디테일 생성
            for (let d of details) {
                await routine_detail_create({
                    r_id: r_id,
                    m_id: Number(d.m_id),
                    step: Number(d.step),
                    sets: Number(d.sets),
                    reps: Number(d.reps),
                    rest_time: Number(d.rest_time),
                    weight: Number(d.weight),
                });
            }

            setOpen(false);

            setName('');
            setP_id("");
            setMachines([]);
            setDetails([
                {
                    m_id: "",
                    step: 1,
                    sets: "",
                    reps: "",
                    rest_time: "",
                    weight: "",
                }
            ])
            
            fetch_routines();
            
        }catch(err){
            console.error(err.response?.data || err);
        }
    };

    // 루틴 삭제
    const handle_delete = async (r_id) =>{
        try {
            await routines_delete(r_id);
            fetch_routines();
        } catch (err) {
            console.error(err.response?.data || err);
        }
    };


  return (
    <div>
        <h1>루틴 관리</h1>

        <button onClick={()=> setOpen(true)}>나만의 루틴 만들기</button>

        {/* 모달 */}
        {open && (
            
            <div>
                <h2>루틴 만들기</h2>
                {/* 루틴 이름 */}
                <input value={name} onChange={(e)=> setName(e.target.value)}
                placeholder='루틴 이름' />

                {/* 부위 선택 */}
                <select value={p_id} onChange={async (e) => {
                    const value = Number(e.target.value);
                    setP_id(value);

                    try{
                        const response = await machines_read(value);
                        setMachines(response.data.data || response.data)
                    }catch (err) {
                        console.error(err.response?.data || err);
                    }
                    setDetails([
                                {
                                    m_id: "",
                                    step: 1,
                                    sets: "",
                                    reps: "",
                                    rest_time: "",
                                    weight:"",
                                }
                            ])
                    }}
                    >
                    <option value="">부위 선택</option>

                    {Array.isArray(parts) && parts.map((p) => (
                        <option key={String(p.p_id)} value={p.p_id} >
                        {p.p_name}
                        </option>
                    ))}
                </select>

                {details.map((d,i) =>(
                    <div key={`${i}-${d.step}`}>
                        <h4>{i+1}번 운동</h4>
                            
                            <select
                                value={d.m_id}
                                onChange={(e) =>
                                    handle_detail_change(i, "m_id", e.target.value)
                                }
                            >
                                <option value="">운동 선택</option>

                                {Array.isArray(machines) && machines.map((m) => (
                                    <option key={String(m.m_id)} value={m.m_id}>
                                        {m.m_name}
                                    </option>
                                ))}
                            </select>

                        <input value={d.sets} placeholder='세트'
                        onChange={(e)=>handle_detail_change(i,"sets",e.target.value)} />

                        <input value={d.reps} placeholder='횟수'
                        onChange={(e)=>handle_detail_change} />

                        <input value={d.weight} placeholder='무게'
                        onChange={(e)=>handle_detail_change(i,"weight",e.target.value)} />

                        <input value={d.rest_time} placeholder='휴식'
                        onChange={(e)=>handle_detail_change(i,'rest_time',e.target.value)} />

                    </div>
                ))}


                <button onClick={handle_add_detail}>운동 추가</button>

                <button onClick={handle_create}>루틴 생성</button>

                <button onClick={()=> setOpen(false)}>닫기</button>
            </div>
        )}


        {/* 루틴 리스트 띄우기 */}
        {
            list.map((routines)=>(
                <div key={String(routines.r_id)}>
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

export default Routines_page