import { useEffect, useState } from "react";
import {
  createComment,
  deleteComment,
  getComments,
  updateComment,
} from "../../api/board";
import { like_comments_count, like_comments_toggle } from "../../api/likes";
import { user_profile } from "../../api/user";
import { useAuth } from "../AuthContext";
import "./Comments.css";

const Comments = ({ b_id }) => {
  const { user } = useAuth();
  const [comments, set_comments] = useState([]);
  const [c_content, set_c_content] = useState("");

  const [edit_id, set_edit_id] = useState(null);
  const [edit_content, set_edit_content] = useState("");

  const fetch_comments = async () => {
    try {
      const result = await getComments(b_id);
      const commentsData = Array.isArray(result) ? result : result.data || [];

      const commentsWithLikes = await Promise.all(
        commentsData.map(async (comment) => {
          try {
            const [countResponse, userResult] = await Promise.all([
              like_comments_count(comment.c_id),
              user_profile(comment.u_id),
            ]);

            return {
              ...comment,
              like_count: countResponse.data || 0,
              u_name: userResult.data.u_name,
            };
          } catch {
            return {
              ...comment,
              like_count: 0,
              u_name: "알 수 없음",
            };
          }
        }),
      );

      set_comments(commentsWithLikes);
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

  const handle_like_toggle = async (c_id) => {
    try {
      const result = await like_comments_toggle(c_id);

      set_comments((prev) =>
        prev.map((comment) =>
          comment.c_id === c_id
            ? {
                ...comment,
                like_count:
                  result.status === "liked"
                    ? comment.like_count + 1
                    : comment.like_count - 1,
              }
            : comment,
        ),
      );
    } catch (error) {
      console.error("좋아요 토글 실패:", error);
      alert("로그인이 필요하거나 요청이 중복되었습니다.");
    }
  };

  return (
    <div className="comments-section">
      <h2 className="comments-title">댓글</h2>

      <form className="comment-form" onSubmit={handle_comment_submit}>
        <input
          className="comment-input"
          value={c_content}
          onChange={(e) => set_c_content(e.target.value)}
          placeholder="댓글을 입력하세요"
        />

        <button className="comment-submit" type="submit">
          댓글 등록
        </button>
      </form>

      {comments.length === 0 ? (
        <p className="comment-content">댓글이 없습니다.</p>
      ) : (
        comments.map((comment) => {
          const is_writer = Number(comment.u_id) === Number(login_user_id);

          return (
            <div className="comment-item" key={comment.c_id}>
              {edit_id === comment.c_id ? (
                <div className="comment-form">
                  <input
                    className="comment-input"
                    value={edit_content}
                    onChange={(e) => set_edit_content(e.target.value)}
                  />

                  <button
                    className="comment-submit"
                    onClick={() => handle_update_comment(comment.c_id)}
                  >
                    저장
                  </button>

                  <button
                    className="comment-submit"
                    onClick={() => set_edit_id(null)}
                  >
                    취소
                  </button>
                </div>
              ) : (
                <>
                  <div className="comment-content">{comment.c_content}</div>

                  <div className="comment-writer">
                    작성자: {comment.u_name}
                  </div>

                  <div className="comment-actions">
                    <button onClick={() => handle_like_toggle(comment.c_id)}>
                      ❤️ {comment.like_count || 0}
                    </button>

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
                </>
              )}
            </div>
          );
        })
      )}
    </div>
  );
};

export default Comments;
