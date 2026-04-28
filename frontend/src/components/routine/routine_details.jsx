import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { routine_detail_read_all } from '../../api/routine_details'
import { machines_read } from '../../api/machines'

const Routine_details = () => {
  
    const {r_id} = useParams();

    const [list,setList] = useState([]);
    const [loading,setLoading] = useState(true);

    const [machines, setMachines] =useState([]);
    const [p_id,setP_id] = useState('');

    const [newform, setNewform] =useState({
        m_id:'',
        step:'',
        sets:'',
        reps:'',
        rest_time:'',
        weight:'',
    });


    useEffect(() => {
        fetch_rotutine_details();
    }, []);

    

        const fetch_rotutine_details = async ()=>{
            try{
                const response = await routine_detail_read_all(r_id);
                
                console.log('운동 데이터', response.data);

                setList(response.data.data);
            }catch (err) {
                console.error('운동 조회 실패',err);
            } finally {
                setLoading(false);
            }
        };
    
        const handleChange = (e) =>{
            const {name,value} = e.target;
            setNewform({
                ...newform,
                [name] : value,
            });
        };

        const handle_Add_new_routine_detail =  async ()=>{
            try{
                await add_new_routine_detail({
                    r_id: Number(r_id),
                    m_id: Number(newform.m_id),
                    step: Number(newform.step),
                    reps: Number(newform.reps),
                    rest_time : Number(newform.rest_time),
                    weight : Number(newform.weight)
                });

                fetch_rotutine_details();

                setNewform({
                    m_id: "",
                    step: "",
                    sets: "",
                    reps: "",
                    rest_time: "",
                    weight:"",
                })
            } catch (err){
                console.error('추가 실패',err);
            }
        }


        const handle_Part_change = async (e)=>{
            const value = e.target.value;

            setP_id(value);

            try{
                const response = await machines_read(value);

                console.log('머신', response.data.data);

                setMachines(response.data.data);
            } catch(err){
                console.error(err);
            }
        }

        if (loading) return <div>로딩중...</div>;

    return (
    <div>
        <h1>루틴 상세</h1>
        {/* 디테일 리스트 */}
        {list.map((r_d)=>(
            <div key={r_d.m_id}>
                <h3>{r_d.m_name}</h3>
                <p>{r_d.sets}세트 x {r_d.reps}회 x {r_d.weight}kg</p>
                <p>휴식 : {r_d.rest_time}초</p>
                <p>부위 : {r_d.p_name}</p>
            </div>
        ))}

        {/* 새 루틴 생성 폼 */}
        {/* <div>
            <h3>운동 추가</h3>

            <input name="m_id" id="" />
        </div> */}
    </div>
  )
}

export default Routine_details