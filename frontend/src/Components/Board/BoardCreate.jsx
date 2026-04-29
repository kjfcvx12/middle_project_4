import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createBoard } from "../../api/board";

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
    <div style={{ paddingBottom: "80px" }}>
      <h1>글쓰기</h1>

      <form onSubmit={handle_submit}>
        <textarea
          value={b_content}
          onChange={(e) => set_b_content(e.target.value)}
          placeholder="내용을 입력하세요"
          rows={10}
          style={{ width: "100%" }}
        />

        <button type="submit">등록</button>
      </form>
    </div>
  );
};

export default BoardCreate;
