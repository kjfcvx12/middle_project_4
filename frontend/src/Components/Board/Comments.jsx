import { useEffect, useState } from "react";
import {
  createComment,
  deleteComment,
  getComments,
  updateComment,
} from "../../api/board";
import { useAuth } from "../AuthContext";

const Comments = ({ b_id }) => {
  const { user } = useAuth();
  const [comments, set_comments] = useState([]);
  const [c_content, set_c_content] = useState("");

  const [edit_id, set_edit_id] = useState(null);
  const [edit_content, set_edit_content] = useState("");

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

  const handle_start_edit = (comment) => {
    set_edit_id(comment.c_id);
    set_edit_content(comment.c_content);
  };

  const handle_update_comment = async (c_id) => {
    if (!edit_content.trim()) {
      alert("댓글 내용을 입력해주세요.");
      return;
    }

    try {
      await updateComment(b_id, c_id, {
        c_content: edit_content,
      });

      alert("댓글 수정 완료");
      set_edit_id(null);
      set_edit_content("");
      fetch_comments();
    } catch (error) {
      console.error("댓글 수정 실패:", error.response?.data || error.message);
      alert("댓글 수정 실패");
    }
  };

  const handle_delete_comment = async (c_id) => {
    const check = window.confirm("댓글을 삭제하시겠습니까?");
    if (!check) return;

    try {
      await deleteComment(b_id, c_id);
      alert("댓글 삭제 완료");
      fetch_comments();
    } catch (error) {
      console.error("댓글 삭제 실패:", error.response?.data || error.message);
      alert("댓글 삭제 실패");
    }
  };
  const login_user_id =
    typeof user === "number"
      ? user
      : user?.u_id || user?.data?.u_id || user?.user?.u_id;

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
        comments.map((comment) => {
          const is_writer = Number(comment.u_id) === login_user_id;

          return (
            <div key={comment.c_id}>
              {edit_id === comment.c_id ? (
                <div>
                  <input
                    value={edit_content}
                    onChange={(e) => set_edit_content(e.target.value)}
                  />

                  <button onClick={() => handle_update_comment(comment.c_id)}>
                    저장
                  </button>

                  <button onClick={() => set_edit_id(null)}>취소</button>
                </div>
              ) : (
                <div>
                  <p>{comment.c_content}</p>
                  <small>작성자 ID: {comment.u_id}</small>

                  {is_writer && (
                    <>
                      <button onClick={() => handle_start_edit(comment)}>
                        수정
                      </button>

                      <button
                        onClick={() => handle_delete_comment(comment.c_id)}
                      >
                        삭제
                      </button>
                    </>
                  )}
                </div>
              )}
            </div>
          );
        })
      )}
    </div>
  );
};

export default Comments;
