import React, { useEffect, useState } from 'react';
import { useAuth } from '../AuthContext';
import { user_del, user_edit, user_me, user_profile } from '../../api/user';
import { Link } from 'react-router-dom';

const Profile = () => {
  const { logout, isLoggedIn, setIsLoggedIn, user } = useAuth();
  const [ currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [openFavorite, setOpenFavorite]=useState(false);
  const [openBoard, setOpenBoard]=useState(false);
  const [openEdit, setOpenEdit]=useState(false);


  // 초기 실행
  useEffect(() => {
    const ProfileUserData = async () => {
      try {
        const profile= await user_profile(user);
        setCurrentUser(profile.data);
      } catch (error) {
        console.error("사용자 정보를 불러오는데 실패했습니다.", error);
      } finally {
        setLoading(false);
        console(profile.data)
      }
    };

    ProfileUserData();
  }, []);


  if (loading) return <div>로딩 중...</div>;
  if (!currentUser) return <div>데이터가 없습니다.</div>;

  
  const favoriteClick=()=>{
    setOpenFavorite(!openFavorite);
  }

  const boardClick=()=>{
    setOpenBoard(!openBoard);
  }

  const profileEdit=()=>{
    setOpenEdit(!openEdit);
  }



  const userDelClick=async()=>{
    if (confirm("정말 탈퇴하시겠습니까?\n탈퇴 후 데이터 복구는 불가능합니다.")) {
      await user_del();
      await logout();
      alert("탈퇴가 완료되었습니다.");
    }
  }

  return (
    <div>
      <header>
          <h1>프로필</h1>
      </header>

      <div>
          <div>
              <h3>{currentUser.u_name}</h3>
              <div>{currentUser.email}</div>
              <div>가입일: {currentUser.signup_date}</div>
          </div>
      </div>

      <div>
          <div>
              <div> 최다 연속일</div>
              <div></div>
          </div>
          <div>
              <div> 총 운동일</div>
              <div></div>
          </div>
      </div>

      <div>
          <div>
              <div onClick={()=>favoriteClick()}>즐겨찾기</div>
              {openFavorite&&(
                <div>
                  <ul>헬스장</ul>
                  <ul>루틴</ul>
                  <ul>기록</ul>
                </div>
              )}
          </div>
          <div>
              <div onClick={()=>boardClick()}>커뮤니티 기록</div>
              {openBoard&&(
                <div>
                  <ul>내 게시글</ul>
                  <ul>내 댓글</ul>
                </div>
              )}
          </div>
          <div>
              <div onClick={()=>profileEdit()}>정보수정</div>
              {openEdit&&(
                <div>
                  <Link to="/profile/edit"><button>내 정보 수정하기</button></Link>
                  <button onClick={()=>userDelClick()}>탈퇴하기</button>
                </div>
              )}
          </div>
      </div>
      <div>
        <button>SNS 연결</button>
      </div>
      <div>
        <button onClick={logout}>로그아웃</button>
      </div>
    </div>
  );
};

export default Profile;
