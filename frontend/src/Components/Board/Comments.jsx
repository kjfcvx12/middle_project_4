import { useEffect, useState } from "react";
import { createComment, getComments } from "../../api/board";

const Comments = ({ b_id }) => {
  const [comments, set_comments] = useState([]);
  const [c_content, set_c_content] = useState("");

  const fetch_comments = async () => {
    try {
      const result = await getComments(b_id);
      set_comments(Array.isArray(result) ? result : result.data || []);
    } catch (error) {
      console.error("댓글 조회 실패:", error);
    }
  };

  useEffect(() => {
    if (b_id) {
      fetch_comments();
    }
  }, [b_id]);

  const handle_comment_submit = async (e) => {
    e.preventDefault();

    if (!c_content.trim()) {
      alert("댓글 내용을 입력해주세요.");
      return;
    }

    try {
      await createComment(b_id, {
        c_content,
      });

      set_c_content("");
      fetch_comments();
    } catch (error) {
      console.error("댓글 작성 실패 전체:", error);
      console.error("댓글 작성 실패 응답:", error.response?.data);
      alert("댓글 작성 실패");
    }
  };

  return (
    <div>
      <h2>댓글</h2>

      <form onSubmit={handle_comment_submit}>
        <input
          value={c_content}
          onChange={(e) => set_c_content(e.target.value)}
          placeholder="댓글을 입력하세요"
        />
        <button type="submit">댓글 등록</button>
      </form>

      {comments.length === 0 ? (
        <p>댓글이 없습니다.</p>
      ) : (
        comments.map((comment) => (
          <div key={comment.c_id}>
            <p>{comment.c_content}</p>
            <small>작성자 ID: {comment.u_id}</small>
          </div>
        ))
      )}
    </div>
  );
};

export default Comments;
