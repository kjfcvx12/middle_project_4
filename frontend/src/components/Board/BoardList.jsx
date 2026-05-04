import { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { createBoard, getBoards } from "../../api/board";
import { user_profile } from "../../api/user";
import BoardDetail from "./BoardDetail";

const BoardList = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const mode = searchParams.get("mode");

  const [boards, set_boards] = useState([]);
  const [page, set_page] = useState(1);
  const [size] = useState(10);
  const [total_count, set_total_count] = useState(0);
  const [b_content, set_b_content] = useState("");

  const total_pages = Math.ceil(total_count / size);

  useEffect(() => {
    if (mode === "create") return;

    const fetch_boards = async () => {
      try {
        const result = await getBoards(page, size);
        console.log("게시글 응답:", result);

        const boards_with_user = await Promise.all(
          (result.data || []).map(async (board) => {
            const writer_id = board.u_id || board.user_id || board.user?.u_id;

            try {
              const userResult = await user_profile(writer_id);

              return {
                ...board,
                u_id: writer_id,
                u_name: userResult.data.u_name,
              };
            } catch (error) {
              console.error("작성자 정보 조회 실패:", error);
              return {
                ...board,
                u_id: writer_id,
                u_name: "알 수 없음",
              };
            }
          }),
        );

        set_boards(boards_with_user);
        set_total_count(result.total_count || 0);
      } catch (error) {
        console.error("게시글 조회 실패:", error);
        set_boards([]);
      }
    };

    fetch_boards();
  }, [page, size, mode]);

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
      set_b_content("");
      navigate("/board");
    } catch (error) {
      console.error("게시글 작성 실패:", error.response?.data || error.message);
      alert("게시글 작성 실패");
    }
  };

  if (mode === "create") {
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
  }
  if (mode === "detail") {
    return <BoardDetail />;
  }

  return (
    <div style={{ paddingBottom: "80px" }}>
      <h1>게시판</h1>

      <Link to="/board?mode=create">글쓰기</Link>

      {boards.map((board) => (
        <div key={board.b_id}>
          <Link to={`/board?mode=detail&id=${board.b_id}`}>
            게시글 번호 {board.b_id}
          </Link>

          <p>{board.b_content}</p>

          <p>
            작성자:{" "}
            <button
              type="button"
              onClick={() => navigate(`/board?mode=profile&u_id=${board.u_id}`)}
              style={styles.userButton}
            >
              {board.u_name || "알 수 없음"}
            </button>
          </p>
        </div>
      ))}

      {total_pages > 0 && (
        <div style={styles.pagination}>
          <button disabled={page === 1} onClick={() => set_page(page - 1)}>
            {"<"}
          </button>

          {Array.from({ length: total_pages }, (_, i) => i + 1).map((p) => (
            <button
              key={p}
              onClick={() => set_page(p)}
              style={p === page ? styles.activePage : {}}
            >
              {p}
            </button>
          ))}

          <button
            disabled={page === total_pages}
            onClick={() => set_page(page + 1)}
          >
            {">"}
          </button>
        </div>
      )}
    </div>
  );
};
const styles = {
  pagination: {
    marginTop: "20px",
    display: "flex",
    gap: "8px",
    justifyContent: "center",
  },

  activePage: {
    backgroundColor: "#ddd",
    fontWeight: "bold",
  },

  userButton: {
    border: "none",
    background: "none",
    color: "blue",
    cursor: "pointer",
    padding: 0,
  },
};

export default BoardList;
