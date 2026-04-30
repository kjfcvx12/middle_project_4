import { useSearchParams } from "react-router-dom";
import BoardDetail from "./BoardDetail";
import BoardList from "./BoardList";
import BoardProfile from "./BoardProfile";

const Board = () => {
  const [searchParams] = useSearchParams();
  const mode = searchParams.get("mode");

  if (mode === "detail") {
    return <BoardDetail />;
  }

  if (mode === "profile") {
    return <BoardProfile />;
  }

  return (
    <div>
      <BoardList />
    </div>
  );
};

export default Board;
