import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { deleteBoard, getBoardDetail, updateBoard } from "../../api/board";
import { user_profile } from "../../api/user";
import { useAuth } from "../AuthContext";
import "./BoardDetail.css";
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
        const boardData = result.data;

        const writer_id =
          boardData.u_id ?? boardData.user_id ?? boardData.user?.u_id;

        try {
          const userResult = await user_profile(writer_id);

          set_board({
            ...boardData,
            u_id: writer_id,
            u_name: userResult.data.u_name,
          });
        } catch (error) {
          console.error("작성자 정보 조회 실패:", error);

          set_board({
            ...boardData,
            u_id: writer_id,
            u_name: "알 수 없음",
          });
        }
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
    <div>
      <h1 className="board-detail-title">게시글 상세</h1>

      <div className="board-detail-card">
        <p className="board-time">게시글 번호: {board.b_id}</p>

        <p className="board-detail-writer">
          작성자:{" "}
          <button
            type="button"
            onClick={() => navigate(`/board?mode=profile&u_id=${board.u_id}`)}
            className="board-detail-writer-button"
          >
            {board.u_name?.trim() ? board.u_name : "알 수 없음"}
          </button>
        </p>

        {is_edit ? (
          <div>
            <textarea
              className="board-detail-edit-textarea"
              value={edit_content}
              onChange={(e) => set_edit_content(e.target.value)}
              rows={10}
            />

            <div className="board-detail-buttons">
              <button onClick={handle_update}>수정 완료</button>
              <button onClick={handle_cancel_edit}>취소</button>
            </div>
          </div>
        ) : (
          <p className="board-detail-content">{board.b_content}</p>
        )}

        <p className="board-time">작성일: {board.created_at}</p>
        <p className="board-time">수정일: {board.updated_at}</p>
      </div>

      <div className="board-detail-buttons">
        {is_writer && (
          <>
            <button
              onClick={() => {
                set_edit_content(board.b_content);
                set_is_edit(true);
              }}
            >
              수정
            </button>

            <button className="danger" onClick={handle_delete}>
              삭제
            </button>
          </>
        )}

        <button
          className="board-detail-back-button"
          onClick={() => navigate("/board")}
        >
          목록으로
        </button>
      </div>

      <Comment b_id={id} />
    </div>
  );
};

export default BoardDetail;
