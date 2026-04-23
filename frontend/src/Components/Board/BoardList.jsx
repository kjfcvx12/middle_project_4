import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const BoardList = () => {
  const [boards, set_boards] = useState([]);
  const [page, set_page] = useState(1);
  const [total_count, set_total_count] = useState(0);

  useEffect(() => {
    const fetch_boards = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8081/boards/boards");
        const result = await response.json();

        set_boards(result.data || []);
        set_page(result.page || 1);
        set_total_count(result.total_count || 0);
      } catch (error) {
        console.error("게시글 조회 실패:", error);
        set_boards([]);
      }
    };

    fetch_boards();
  }, []);

  return (
    <div style={{ paddingBottom: "80px" }}>
      <h1>커뮤니티 게시판</h1>
      <p>현재 페이지: {page}</p>
      <p>전체 게시글 수: {total_count}</p>

      <Link to="/board/create">글쓰기</Link>

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
