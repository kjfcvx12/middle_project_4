import Gym from "../components/gym/Gym"
import MachineList from '../routine/machine/machine_list';
import MachineDetail from '../routine/machine/machine_detail';
import MachineCreate from '../routine/machine/machine_create';
import { Routes, Route } from "react-router-dom";


const Router=()=>{
    return(
        <Routes>

        {/* 운동기구 생성 */}
        <Route path="/gyms/:g_id/machines/create" element={<MachineCreate />} />

        {/* 운동기구 수정 */}
        <Route path="/gyms/:g_id/machines/edit/:m_id" element={<MachineCreate />} />

        {/* 운동기구 디테일 */}
        <Route path="/gyms/:g_id/machines/:m_id" element={<MachineDetail />} />

        {/* 운동기구 목록 */}
        <Route path="/gyms/:g_id/machines" element={<MachineList />} />

        
        </Routes>
    )
}

export default Router;