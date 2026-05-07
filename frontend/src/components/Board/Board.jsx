import { useSearchParams } from "react-router-dom";
import "./Board.css";
import BoardCreate from "./BoardCreate";
import BoardDetail from "./BoardDetail";
import BoardList from "./BoardList";
import BoardProfile from "./BoardProfile";

const Board = () => {
  const [searchParams] = useSearchParams();
  const mode = searchParams.get("mode");

  return (
    <div className="board-page">
      <div className="board-inner">
        {mode === "create" ? (
          <BoardCreate />
        ) : mode === "detail" ? (
          <BoardDetail />
        ) : mode === "profile" ? (
          <BoardProfile />
        ) : (
          <BoardList />
        )}
      </div>
    </div>
  );
};

export default Board;
