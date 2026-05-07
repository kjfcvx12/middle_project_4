import { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { getBoards } from "../../api/board";
import { like_boards_count, like_boards_toggle } from "../../api/likes";
import { user_profile } from "../../api/user";
import BoardDetail from "./BoardDetail";
import "./BoardList.css";

const BoardList = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const mode = searchParams.get("mode");

  const [boards, set_boards] = useState([]);
  const [page, set_page] = useState(1);
  const [size] = useState(10);
  const [total_count, set_total_count] = useState(0);

  const total_pages = Math.ceil(total_count / size);

  const [keyword, set_keyword] = useState("");
  const [search_keyword, set_search_keyword] = useState("");

  useEffect(() => {
    if (mode === "create") return;

    const fetch_boards = async () => {
      try {
        const result = await getBoards(
          page,
          size,
          search_keyword,
          "created_at,desc",
        );

        const boards_with_info = await Promise.all(
          (result.data || []).map(async (board) => {
            const writer_id = board.u_id || board.user_id || board.user?.u_id;

            try {
              const [userResult, likeCount] = await Promise.all([
                user_profile(writer_id),
                like_boards_count(board.b_id),
              ]);

              return {
                ...board,
                u_id: writer_id,
                u_name: userResult.data.u_name,
                like_count: likeCount,
              };
            } catch (error) {
              console.error("추가 정보 조회 실패:", error);
              return {
                ...board,
                u_id: writer_id,
                u_name: "알 수 없음",
                like_count: 0,
              };
            }
          }),
        );

        set_boards(boards_with_info);
        set_total_count(result.total_count || 0);
      } catch (error) {
        console.error("게시글 조회 실패:", error);
        set_boards([]);
      }
    };

    fetch_boards();
  }, [page, size, mode, search_keyword]);

  if (mode === "detail") {
    return <BoardDetail />;
  }

  const handle_like_toggle = async (b_id) => {
    try {
      const result = await like_boards_toggle(b_id);

      set_boards((prev) =>
        prev.map((board) =>
          board.b_id === b_id
            ? {
                ...board,
                like_count:
                  result.status === "liked"
                    ? board.like_count + 1
                    : board.like_count - 1,
              }
            : board,
        ),
      );
    } catch (error) {
      console.error("좋아요 토글 실패:", error);
      alert("로그인이 필요하거나 요청이 중복되었습니다.");
    }
  };

  return (
    <div style={{ paddingBottom: "80px" }}>
      <Link className="board-write-button" to="/board?mode=create">
        글쓰기
      </Link>

      <form
        className="board-search-form"
        onSubmit={(e) => {
          e.preventDefault();
          set_page(1);
          set_search_keyword(keyword);
        }}
      >
        <input
          className="board-search-input"
          value={keyword}
          onChange={(e) => set_keyword(e.target.value)}
          placeholder="게시글 검색"
        />

        <div className="board-search-buttons">
          <button className="board-search-button" type="submit">
            검색
          </button>

          <button
            className="board-reset-button"
            type="button"
            onClick={() => {
              set_keyword("");
              set_search_keyword("");
              set_page(1);
            }}
          >
            초기화
          </button>
        </div>
      </form>

      {boards.map((board) => (
        <div className="board-card" key={board.b_id}>
          <div className="board-card-header">
            <div className="board-avatar">
              {(board.u_name || "?").slice(0, 1)}
            </div>

            <div className="board-writer-box">
              <button
                type="button"
                onClick={() =>
                  navigate(`/board?mode=profile&u_id=${board.u_id}`)
                }
                className="board-writer-button"
              >
                {board.u_name || "알 수 없음"}
              </button>
            </div>
          </div>

          <Link
            className="board-content"
            to={`/board?mode=detail&id=${board.b_id}`}
          >
            {board.b_content}
          </Link>

          <div className="board-actions">
            <button
              className="board-like-button"
              onClick={() => handle_like_toggle(board.b_id)}
            >
              ❤️ {board.like_count || 0}
            </button>
          </div>
        </div>
      ))}

      {total_pages > 0 && (
        <div className="board-pagination">
          <button disabled={page === 1} onClick={() => set_page(page - 1)}>
            {"<"}
          </button>

          {Array.from({ length: total_pages }, (_, i) => i + 1).map((p) => (
            <button
              key={p}
              onClick={() => set_page(p)}
              className={p === page ? "active" : ""}
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

export default BoardList;
