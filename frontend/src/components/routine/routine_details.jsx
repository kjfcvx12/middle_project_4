import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { routine_detail_create, routine_detail_read_all } from '../../api/routine_details';
import { getParts } from '../../api/parts';
import { machines_read } from './../../api/machines';




const Routine_details = () => {
    
    const {r_id} = useParams();

    const [list,setList] = useState([]);
    const [parts,setParts] = useState([]);
    const [machines,setMachines] = useState([]);

    const [p_id, setP_id]= useState('');

    const [form,setForm] = useState({
        m_id:'',
        step:'',
        sets:'',
        reps:'',
        rest_time:'',
        weight:'',
    });

    useEffect(()=>{
        fetch_routine_details();
        fetch_parts();
    }, []);
  
    // 루틴 디테일 리스트
    const fetch_routine_details = async () => {
        try{
            const response = await routine_detail_read_all(r_id);
            setList(response.data.data);
        } catch (err){
            console.error(err);
        }
    };

    const fetch_parts = async ()=>{
        try{
            const response = await getParts();
            setParts(response.data);
        } catch (err){
            console.error(err);
        }
    };

    // 부위 선택 -> 머신 가져오기
    const handle_part_change = async (e) =>{
        const value = e.target.value;
        setP_id(value);

        try{
            const response = await machines_read(value);
            setMachines(response.data.data);
        } catch (err) {
            console.error(err);
        }
        setForm((perv) = ({...perv, m_id}));
    };

    const handle_change = (e)=>{
        const{name, value} = e.target;

        setForm({
            ...form,
            [name]:value,
        });
    };
  
    // 루틴 디테일 추가
    const handleAdd = async () => {
        try{
            await routine_detail_create({
                r_id: Number(r_id),
                m_id: Number(form.m_id),
                step: Number(form.step),
                sets: Number(form.sets),
                reps: Number(form.reps),
                rest_time: Number(form.rest_time),
                weight: Number(form.weight),
            });

            fetch_routine_details();

            setForm({
                m_id: "",
                step: "",
                sets: "",
                reps: "",
                rest_time: "",
                weight:"",
            });
        }catch (err){
            console.error(err);
        }
    };


  
    return (
    <div>
        <h1>루틴 상세</h1>
        <div>
            <h3>운동 루틴 추가</h3>
            {/* 부위 */}
            <select value={p_id} onChange={handle_part_change}>
                <option value="">부위 선택</option>
                {parts.map((part) => (
                    <option key={part.p_id} value={part.p_id}>
                        {part.p_name}
                    </option>
                ))}
            </select>

            <select name="m_id" value={form.m_id} onChange={handle_change}>
                <option value="">운동 선택</option>
                {machines.map((machine)=>(
                    <option key={machine.m_id} value={machine.m_id}>{machine.m_name}</option>
                ))}
            </select>

            <input name="step" placeholder="순서" value={form.step} onChange={handle_change} />
            <input name="sets" placeholder="세트" value={form.sets} onChange={handle_change} />
            <input name="reps" placeholder="횟수" value={form.reps} onChange={handle_change} />
            <input name="rest_time" placeholder="휴식" value={form.rest_time} onChange={handle_change} />
            <input name="weight" placeholder="무게" value={form.weight} onChange={handle_change} />
            
            <button onClick={handleAdd}>추가</button>

        </div>
        {/* 리스트 */}
        {list.map((ex)=>(
            <div key={ex.m_id}>
                <h3>{ex.m_name}</h3>
                <p>{ex.sets}세트 x {ex.reps}회 x {ex.weight}kg</p>
            </div>
        ))}

    </div>
  )
}

export default Routine_details