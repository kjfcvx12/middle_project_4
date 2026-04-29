import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { createComment, getBoardDetail, getComments } from "../../api/board";

const BoardDetail = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const id = searchParams.get("id");

  const [board, set_board] = useState(null);
  const [comments, set_comments] = useState([]);
  const [c_content, set_c_content] = useState("");

  useEffect(() => {
    const fetch_board_detail = async () => {
      try {
        const result = await getBoardDetail(id);
        set_board(result.data);
      } catch (error) {
        console.error("게시글 상세 조회 실패:", error);
      }
    };

    const fetch_comments = async () => {
      try {
        const result = await getComments(id);

        console.log("댓글 응답:", result);

        set_comments(Array.isArray(result) ? result : result.data || []);
      } catch (error) {
        console.error("댓글 조회 실패:", error);
      }
    };

    if (id) {
      fetch_board_detail();
      fetch_comments();
    }
  }, [id]);

  const handle_comment_submit = async (e) => {
    e.preventDefault();

    if (!c_content.trim()) {
      alert("댓글 내용을 입력해주세요.");
      return;
    }

    try {
      await createComment(id, 1, {
        c_content,
      });

      set_c_content("");

      const comment_result = await getComments(id);

      set_comments(
        Array.isArray(comment_result)
          ? comment_result
          : comment_result.data || [],
      );
    } catch (error) {
      console.error("댓글 작성 실패:", error);
      alert("댓글 작성 실패");
    }
  };

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

      <h2>댓글</h2>

      <form onSubmit={handle_comment_submit}>
        <input
          value={c_content}
          onChange={(e) => set_c_content(e.target.value)}
          placeholder="댓글을 입력하세요"
        />
        <button type="submit">댓글 등록</button>
      </form>

      {comments.map((comment) => (
        <div key={comment.c_id}>
          <p>{comment.c_content}</p>
          <small>작성자 ID: {comment.u_id}</small>
        </div>
      ))}

      <button onClick={() => navigate("/board")}>목록으로</button>
    </div>
  );
};

export default BoardDetail;
