import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createBoard } from "../../api/board";
import "./BoardCreate.css";

const BoardCreate = () => {
  const navigate = useNavigate();
  const [b_content, set_b_content] = useState("");

  const handle_submit = async (e) => {
    e.preventDefault();

    if (!b_content.trim()) {
      alert("내용을 입력해주세요.");
      return;
    }

    try {
      await createBoard({
        b_content,
      });

      alert("게시글 작성 완료");
      navigate("/board");
    } catch (error) {
      console.error("게시글 작성 실패:", error.response?.data || error.message);
      alert("게시글 작성 실패");
    }
  };

  return (
    <div className="board-create-card">
      <h1 className="board-create-title">글쓰기</h1>

      <form className="board-create-form" onSubmit={handle_submit}>
        <textarea
          className="board-create-textarea"
          value={b_content}
          onChange={(e) => set_b_content(e.target.value)}
          placeholder="내용을 입력하세요"
          rows={10}
        />

        <div className="board-create-buttons">
          <button type="submit">등록</button>
          <button type="button" onClick={() => navigate("/board")}>
            취소
          </button>
        </div>
      </form>
    </div>
  );
};

export default BoardCreate;
