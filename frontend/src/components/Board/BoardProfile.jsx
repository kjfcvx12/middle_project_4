import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { user_profile } from "../../api/user";
import "./BoardProfile.css";

const BoardProfile = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const u_id = searchParams.get("u_id");
  const [profile, set_profile] = useState(null);

  useEffect(() => {
    const fetch_profile = async () => {
      try {
        const result = await user_profile(u_id);
        set_profile(result.data);
      } catch (error) {
        console.error(
          "유저 프로필 조회 실패:",
          error.response?.data || error.message,
        );
      }
    };

    if (u_id) fetch_profile();
  }, [u_id]);

  if (!u_id) return <div>유저 ID가 없습니다.</div>;
  if (!profile) return <div>로딩 중...</div>;

  return (
  <div className="profile-card">
    <h1 className="profile-title">유저 정보</h1>

    <div className="profile-avatar">
      {(profile.u_name || "?").slice(0, 1)}
    </div>

    <div className="profile-name">
      {profile.u_name}
    </div>

    <div className="profile-email">
      {profile.email}
    </div>

    <div className="profile-info">
      <p>가입일: {profile.signup_date}</p>
    </div>

    <div className="board-detail-buttons">
      <button
        onClick={() =>
          navigate(`/note/create?u_id=${u_id}&email=${profile.email}`)
        }
      >
        메시지 보내기
      </button>

      <button onClick={() => navigate(-1)}>
        뒤로가기
      </button>
    </div>
  </div>
);
};

export default BoardProfile;
