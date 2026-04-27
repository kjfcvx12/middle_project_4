import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const BoardList = () => {
  const [boards, set_boards] = useState([]);
  const [page, set_page] = useState(1);
  const [size] = useState(10);
  const [total_count, set_total_count] = useState(0);
  const total_pages = Math.ceil(total_count / size);

  useEffect(() => {
    const fetch_boards = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8081/boards?page=${page}&size=${size}`,
        );
        const result = await response.json();

        set_boards(result.data || []);
        set_total_count(result.total_count || 0);
      } catch (error) {
        console.error("게시글 조회 실패:", error);
        set_boards([]);
      }
    };

    fetch_boards();
  }, [page, size]);

  return (
    <div style={{ paddingBottom: "80px" }}>
      <h1>게시판</h1>

      <Link to="/boards/create">글쓰기</Link>

      {boards.map((board) => (
        <div key={board.b_id}>
          <Link to={`/board/${board.b_id}`}>게시글 번호 {board.b_id}</Link>
          <p>{board.b_content}</p>
        </div>
      ))}
    </div>
  );
};

export default BoardList;
