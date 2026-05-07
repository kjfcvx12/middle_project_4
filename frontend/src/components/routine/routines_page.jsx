import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { routines_read,routines_create,routines_delete,routine_random_create  } from '../../api/routines';
import { getParts } from '../../api/parts';
import { routine_detail_create, routine_detail_read_all } from './../../api/routine_details';
import { machines_read } from './../../api/machines';
import './Routines_page.css';


const Routines_page = () => {
    // console.log("🔥 API 호출됨");
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

    const [fullList,setFullList]=useState([]);

    const [selectedPart,setSelectedPart] = useState('');
    const [count, setCount] = useState(3);


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

            const result = await Promise.all(
                response.data.data.map(async (r)=>{

                    const detailRes = await routine_detail_read_all(r.r_id);
                    const details = detailRes.data.data || [];

                    const totalVolume = details.reduce((acc,d) =>{
                        return acc + (d.sets * d.reps * (d.weight || 0));
                    }, 0)

                    return{
                        ...r,
                        details,
                        totalVolume,
                        count : details.length,
                    }
                })
            );
            
            setFullList(result)





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



    // 랜덤 루틴 생성
    const handle_random = async ()=>{
        if (!selectedPart){
            alert ("부위를 선택하세요")
            return ;
        }

        try{
            await routine_random_create(selectedPart,count);

            fetch_routines();
        }catch(err){
            console.error(err);
        }
    }    


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

    const handle_detail_change = (index, key, value) => {
    setDetails(prev =>
        prev.map((item, i) =>
            i === index
                ? { ...item, [key]: value }
                : item
        )
    );
};

    // 루틴/디테일 생성
    const handle_create = async()=>{
        if(!name || !p_id){
            alert('루틴 이름과 부위를 설정하세요')
            return;
        } 
        
    
        try{
            // 루틴 생성
            const response = await routines_create(
                {r_name : name,
                p_id: Number(p_id),
                }
            );

            const r_id = response.data.r_id;

            // 루틴 디테일 생성
            for (let i = 0; i < details.length; i++) {
                const d = details[i];


                if (!d.m_id || !d.sets || !d.reps || !d.rest_time) {
                    alert("운동 / 세트 / 횟수 / 휴식 전부 숫자만 입력해야 합니다");
                    return;
                }

                await routine_detail_create({
                    r_id: r_id,
                    m_id: Number(d.m_id),
                    step: i + 1, 
                    sets: Number(d.sets || 0),
                    reps: Number(d.reps || 0),
                    rest_time: Number(d.rest_time || 0),
                    weight: Number(d.weight || 0),
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
    <div className='routine-page'>
        <h1>루틴 관리</h1>

        

        {fullList.map((r)=>(
            <div key={r.r_id} className='routine-card'>

                <h2 onClick={()=> nav(`/routine/${r.r_id}`)}>
                    {r.r_name}
                </h2>

                <p>총 볼륨 : {r.totalVolume.toLocaleString()} kg</p>

                <p>{r.count}개 운동</p>

                <button className='delete-btn' onClick={()=>handle_delete(r.r_id)}>
                    삭제
                </button>

                <hr />

                {r.details.map((d,i)=>(
                    <div key={`${d.m_id}-${i}`} className='exercise-item'>
                        <strong>{d.m_name}</strong>
                        <div>
                            {d.sets}세트 x {d.reps}회 x {d.weight || 0}kg
                        </div>
                        
                    </div>
                ))}



            </div>
        ))}


        <h3>추천 루틴 생성</h3>

        <div className='recommend-box'>

            <select
                value={selectedPart}
                onChange={(e) => setSelectedPart(e.target.value)}
            >
                <option value="">부위 선택</option>
                
                {parts.map((p)=>(
                    <option key={p.p_id} value={p.p_name}>
                        {p.p_name}
                    </option>
                ))}
            </select>

            <div className='count-wrap'>

    <span>운동 갯수</span>

    <input
    className='count-input'
    type="number"
    value={count}
    min={1}
    max={6}

    style={{
    width:'110px',
    minWidth:'110px',
    maxWidth:'110px',
    height:'44px',
    padding:'0 12px',
    margin:'0 auto',
    display:'block',
    textAlign:'center',
    boxSizing:'border-box',
    borderRadius:'14px'
}}

    onChange={(e)=> setCount(Number(e.target.value))}
/>

</div>

            <button
                className='recommend-btn'
                onClick={handle_random}
            >
                추천 루틴 생성
            </button>

        </div>


        <br />

        <button className='create-btn' onClick={()=> setOpen(true)}>
            + 나만의 루틴 만들기
        </button>

        {/* 모달 */}
        {open && (
            
            <div className='modal-box'>
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
                    <div key={`${i}-${d.step}`} className='detail-card'>
                        <h4>{i+1}번 운동</h4>
                            
                            <select
                                value={d.m_id}
                                onChange={(e) =>
                                    handle_detail_change(i, "m_id", e.target.value)
                                }
                            >
                                운동 선택 : <option value="">운동 선택</option>

                                {Array.isArray(machines) && machines.map((m) => (
                                    <option key={String(m.m_id)} value={m.m_id}>
                                        {m.m_name}
                                    </option>
                                ))}
                            </select>
                                <br />
                        세트 수: <input value={d.sets} placeholder='세트'
                        onChange={(e)=>handle_detail_change(i,"sets",e.target.value)} />
                        <br />
                        반복 횟수 :<input value={d.reps} placeholder='횟수'
                        onChange={(e)=>handle_detail_change(i,"reps",e.target.value)} />
                        <br />
                        중량 :<input value={d.weight} placeholder='무게'
                        onChange={(e)=>handle_detail_change(i,"weight",e.target.value)} />
                        <br />
                        휴식 시간:<input value={d.rest_time} placeholder='휴식'
                        onChange={(e)=>handle_detail_change(i,'rest_time',e.target.value)} />
                        <br />
                    </div>
                ))}


                <button className='add-btn' onClick={handle_add_detail}>
                    운동 추가
                </button>

                <button className='submit-btn' onClick={handle_create}>
                    루틴 생성
                </button>

                <button className='close-btn' onClick={()=> setOpen(false)}>
                    닫기
                </button>
            </div>
        )}
    </div>
  )
}

export default Routines_page