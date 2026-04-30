import React, { useEffect, useState } from 'react';
import { useAuth } from '../AuthContext';
import { user_del, user_edit, user_me, user_profile } from '../../api/user';
import { Link } from 'react-router-dom';
import { user_get_favorite_gyms, user_get_favorite_machines, user_get_favorite_routines } from './../../api/user';

const Profile = () => {
  const { logout, userData} = useAuth();

  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const [openFavorite, setOpenFavorite]=useState(false);
  const [favGyms, setFavGyms] = useState([]);
  const [favMachines, setFavMachines] = useState([]);
  const [favRoutines, setFavRoutines] = useState([]);


  const [openBoard, setOpenBoard]=useState(false);
  const [myBoard, setMyBoard]=useState([]);
  const [myComment, setMyComment]=useState([]);

  const [openEdit, setOpenEdit]=useState(false);




  // 현재 사용자 업데이트
  useEffect(() => {
    if (userData) {
      setCurrentUser(userData);
      setLoading(false);
    }
  }, [userData]);


  if (loading) return <div>로딩 중...</div>;
  if (!currentUser) return <div>데이터가 없습니다.</div>;

  
  const favoriteClick=async ()=>{
    setOpenFavorite(!openFavorite);
    setFavGyms([]);
    setFavMachines([]);
    setFavRoutines([]);
    if (!openFavorite) {
      try {
        const currentId = currentUser.u_id; 

        const FavGymsList = await user_get_favorite_gyms(currentId);
        const FavMachineList = await user_get_favorite_machines(currentId);
        const FavRoutineList = await user_get_favorite_routines(currentId);

        setFavGyms(FavGymsList.data.length === 0 ? ['즐겨찾기한 체육관이 없습니다.'] : FavGymsList.data);
        setFavMachines(FavMachineList.data.length === 0 ? ['즐겨찾기한 운동기구가 없습니다.'] : FavMachineList.data);
        setFavRoutines(FavRoutineList.data.length === 0 ? ['즐겨찾기한 루틴이 없습니다.'] : FavRoutineList.data);


      } catch (error) {
          console.error("데이터를 가져오는 중 오류 발생", error);
      }
    }
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
                  <div>
                    <div>헬스장</div>
                    {favGyms.map((gym, i) => (
                      <div key={i}>{gym.g_name || gym}</div> 
                    ))}
                  </div>
                  <div>
                    <div>루틴</div>
                    {favMachines.map((machine, i) => (
                      <div key={i}>{machine.m_name || machine}</div>
                    ))}
                  </div>
                  <div>
                    <div>기록</div>
                    {favRoutines.map((Routine, i) => (
                      <div key={i}>{Routine.r_name || Routine}</div>
                    ))}
                  </div>
                </div>
              )}
          </div>
          <div>
              <div onClick={()=>boardClick()}>커뮤니티 기록</div>
              {openBoard&&(
                <div>
                  <div>내 게시글</div>
                  <div>내 댓글</div>
                </div>
              )}
          </div>
          <div>
              <div onClick={()=>profileEdit()}>정보수정</div>
              {openEdit&&(
                <div>
                  <div><Link to="/profile/edit"><button>내 정보 수정하기</button></Link></div>
                  <div><button onClick={()=>userDelClick()}>탈퇴하기</button></div>
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
