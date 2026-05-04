import { useNavigate } from "react-router-dom";

const Gym = () => {
  const nav = useNavigate();

  return(
    <div>
      <h1>헬스장</h1>

      <button onClick={()=>nav("/machines")}>
        운동기구 목록 보기
      </button>
    </div>
  );
};

export default Gym;