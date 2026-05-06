import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { user_profile } from "../../api/user";

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
    <div>
      <h1>유저 정보</h1>

      <p>이름: {profile.u_name}</p>
      <p>이메일: {profile.email}</p>
      <p>가입일: {profile.signup_date}</p>

      <button onClick={() => navigate(`/message?u_id=${u_id}`)}>
        메시지 보내기
      </button>

      <button onClick={() => navigate(-1)}>뒤로가기</button>
    </div>
  );
};

export default BoardProfile;