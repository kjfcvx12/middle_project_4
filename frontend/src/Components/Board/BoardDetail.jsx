import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { getBoardDetail } from "../../api/board";
import Comment from "./Comments";

const BoardDetail = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const id = searchParams.get("id");

  const [board, set_board] = useState(null);

  useEffect(() => {
    const fetch_board_detail = async () => {
      try {
        const result = await getBoardDetail(id);
        set_board(result.data);
      } catch (error) {
        console.error("게시글 상세 조회 실패:", error);
      }
    };

    if (id) {
      fetch_board_detail();
    }
  }, [id]);

  if (!id) {
    return <div style={{ paddingBottom: "80px" }}>게시글 ID가 없습니다.</div>;
  }

  if (!board) {
    return <div style={{ paddingBottom: "80px" }}>로딩 중...</div>;
  }

  return (
    <div style={{ paddingBottom: "80px" }}>
      <h1>게시글 상세</h1>

      <p>게시글 번호: {board.b_id}</p>
      <p>작성자 ID: {board.u_id}</p>
      <p>내용: {board.b_content}</p>
      <p>작성일: {board.created_at}</p>
      <p>수정일: {board.updated_at}</p>

      <hr />

      <Comment b_id={id} />

      <button onClick={() => navigate("/board")}>목록으로</button>
    </div>
  );
};

export default BoardDetail;
