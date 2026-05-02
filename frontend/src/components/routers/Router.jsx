import Gym from "../components/gym/Gym"
import machine_detail from '../routine/machine/machine_detail';
import machine_list from '../routine/machine/machine_list';


const Router=()=>{
    return(
        <Routes>

        {/* Gym */}
        <Route path="/" element={<Gym />} />

        {/* 운동기구 목록 */}
        <Route path="/machines" element={<MachineList />} />

        {/* 운동기구 디테일 */}
        <Route path="/machines/:m_id" element={<MachineDetail />} />

        {/* 운동기구 생성 */}
        <Route path="/machines/create" element={<MachineCreate />} />

        {/* 운동기구 수정 */}
        <Route path="/machines/edit/:m_id" element={<MachineCreate />} />

        </Routes>
    )
}

export default Router;