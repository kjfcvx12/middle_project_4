import { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { createBoard, getBoards } from "../../api/board";
import BoardDetail from "./BoardDetail";

const Board = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const mode = searchParams.get("mode");

  const [boards, set_boards] = useState([]);
  const [page, set_page] = useState(1);
  const [size] = useState(10);
  const [total_count, set_total_count] = useState(0);
  const [b_content, set_b_content] = useState("");

  const total_pages = Math.ceil(total_count / size);

  useEffect(() => {
    if (mode === "create") return;

    const fetch_boards = async () => {
      try {
        const result = await getBoards(page, size);

        set_boards(result.data || []);
        set_total_count(result.total_count || 0);
      } catch (error) {
        console.error("게시글 조회 실패:", error);
        set_boards([]);
      }
    };

    fetch_boards();
  }, [page, size, mode]);

  const handle_submit = async (e) => {
    e.preventDefault();

    if (!b_content.trim()) {
      alert("내용을 입력해주세요.");
      return;
    }

    try {
      await createBoard(1, {
        b_content,
      });

      alert("게시글 작성 완료");
      navigate("/board");
    } catch (error) {
      console.error("게시글 작성 실패:", error.response?.data || error.message);
      alert("게시글 작성 실패");
    }
  };

  if (mode === "create") {
    return (
      <div style={{ paddingBottom: "80px" }}>
        <h1>글쓰기</h1>

        <form onSubmit={handle_submit}>
          <textarea
            value={b_content}
            onChange={(e) => set_b_content(e.target.value)}
            placeholder="내용을 입력하세요"
            rows={10}
            style={{ width: "100%" }}
          />

          <button type="submit">등록</button>
        </form>
      </div>
    );
  }
  if (mode === "detail") {
    return <BoardDetail />;
  }

  return (
    <div style={{ paddingBottom: "80px" }}>
      <h1>게시판</h1>

      <Link to="/board?mode=create">글쓰기</Link>

      {boards.map((board) => (
        <div key={board.b_id}>
          <Link to={`/board?mode=detail&id=${board.b_id}`}>
            게시글 번호 {board.b_id}
          </Link>
          <p>{board.b_content}</p>
        </div>
      ))}
    </div>
  );
};

export default Board;