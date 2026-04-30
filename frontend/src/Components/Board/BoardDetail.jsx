import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { deleteBoard, getBoardDetail, updateBoard } from "../../api/board";
import { useAuth } from "../AuthContext";
import Comment from "./Comments";

const BoardDetail = () => {
  const { user } = useAuth();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const id = searchParams.get("id");

  const [board, set_board] = useState(null);
  const [is_edit, set_is_edit] = useState(false);
  const [edit_content, set_edit_content] = useState("");

  useEffect(() => {
    const fetch_board_detail = async () => {
      try {
        const result = await getBoardDetail(id);
        console.log("상세 게시글 응답:", result);
        console.log("상세 게시글 data:", result.data);
        set_board(result.data);
        set_board(result.data);
      } catch (error) {
        console.error("게시글 상세 조회 실패:", error);
      }
    };

    if (id) {
      fetch_board_detail();
    }
  }, [id]);

  const handle_delete = async () => {
    const check = window.confirm("게시글을 삭제하시겠습니까?");

    if (!check) return;

    try {
      await deleteBoard(id);
      alert("게시글 삭제 완료");
      navigate("/board");
    } catch (error) {
      console.error("게시글 삭제 실패:", error.response?.data || error.message);
      alert("게시글 삭제 실패");
    }
  };

  const handle_update = async () => {
    if (!edit_content.trim()) {
      alert("수정할 내용을 입력해주세요.");
      return;
    }

    try {
      const result = await updateBoard(id, {
        b_content: edit_content,
      });

      alert("게시글 수정 완료");

      set_board(result.data);
      set_is_edit(false);
    } catch (error) {
      console.error("게시글 수정 실패:", error.response?.data || error.message);
      alert("게시글 수정 실패");
    }
  };

  const handle_cancel_edit = () => {
    set_edit_content(board.b_content);
    set_is_edit(false);
  };

  if (!id) {
    return <div style={{ paddingBottom: "80px" }}>게시글 ID가 없습니다.</div>;
  }

  if (!board) {
    return <div style={{ paddingBottom: "80px" }}>로딩 중...</div>;
  }

  const login_user_id =
    typeof user === "number"
      ? user
      : user?.u_id || user?.data?.u_id || user?.user?.u_id;

  const is_writer = Number(board.u_id) === Number(login_user_id);

  return (
    <div style={{ paddingBottom: "80px" }}>
      <h1>게시글 상세</h1>

      <p>게시글 번호: {board.b_id}</p>
      <p>
        작성자:{" "}
        <button
          type="button"
          onClick={() => navigate(`/profile?u_id=${board.u_id}`)}
          style={styles.userButton}
        >
          {board.u_name || `회원 ${board.u_id}`}
        </button>
      </p>

      {is_edit ? (
        <div>
          <textarea
            value={edit_content}
            onChange={(e) => set_edit_content(e.target.value)}
            rows={10}
            style={{ width: "100%" }}
          />

          <button onClick={handle_update}>수정 완료</button>
          <button onClick={handle_cancel_edit}>취소</button>
        </div>
      ) : (
        <div>
          <p>내용: {board.b_content}</p>

          {is_writer && (
            <button
              onClick={() => {
                set_edit_content(board.b_content);
                set_is_edit(true);
              }}
            >
              수정
            </button>
          )}
        </div>
      )}

      <p>작성일: {board.created_at}</p>
      <p>수정일: {board.updated_at}</p>

      <hr />

      <Comment b_id={id} />

      {is_writer && <button onClick={handle_delete}>삭제</button>}
      <button onClick={() => navigate("/board")}>목록으로</button>
    </div>
  );
};

const styles = {
  userButton: {
    border: "none",
    background: "none",
    color: "blue",
    cursor: "pointer",
    padding: 0,
  },
};

export default BoardDetail;
