import React, { useEffect, useState } from 'react';
import { useAuth } from '../AuthContext';
import { user_del, user_edit, user_me, user_profile } from '../../api/user';
import { Link, data } from 'react-router-dom';
import { user_get_favorite_gyms, user_get_favorite_machines, user_get_favorite_routines } from './../../api/user';
import { note_create } from '../../api/notes';
import { gyms_detail } from '../../api/gyms';
import { getLogs } from '../../api/logApi';
import "./Profile.css"

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

  const [gymNames, setGymNames] = useState({});

  const [exCount, setExCount]= useState(0);


  useEffect(() => {
  const loadUser = async () => {
    try {
      const res = await user_me();
      const pro=await user_profile(res)
      setCurrentUser(pro.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  loadUser();
}, []);


  // 현재 사용자 업데이트
  useEffect(() => {
    if (userData) {
      setCurrentUser(userData);
      setLoading(false);
    }
  }, [userData]);

  useEffect(() => {
  const fetchLogs = async () => {
    try {
      const logData = await getLogs();

      if (Array.isArray(logData)) {

        const dates = logData.map(log => log.log_date.split('T')[0]);
        
        const uniqueDates = [...new Set(dates)];
           
        setExCount(uniqueDates.length);
      } else {
        setExCount(0);
      }
    } catch (error) {
      console.error("로그 로딩 실패", error);
    }
  };
  fetchLogs();
}, []);


 useEffect(() => {
    const fetchNames = async () => {
      const actualGyms = favGyms.filter(gym => typeof gym === 'object' && gym.g_id);
      if (actualGyms.length === 0) return;

      const newNames = { ...gymNames };
      for (const gym of actualGyms) {
        if (!newNames[gym.g_id]) {
          try {
            const detail = await gyms_detail(gym.g_id);
            newNames[gym.g_id] = detail.g_name;
          } catch (err) {
            newNames[gym.g_id] = "없음";
          }
        }
      }
      setGymNames(newNames);
    };
    fetchNames();
  }, [favGyms]); 


  if (loading) return <div>로딩 중...</div>;
  if (!currentUser) return <div>데이터가 없습니다.</div>;

  
  const favoriteClick=async ()=>{
    const nextState = !openFavorite;
    setOpenFavorite(nextState);

    if (!nextState) {
      try {
        const currentId = currentUser.u_id; 

        const FavGymsList = await user_get_favorite_gyms(currentId);
        const FavMachineList = await user_get_favorite_machines(currentId);
        const FavRoutineList = await user_get_favorite_routines(currentId);

        setFavGyms(FavGymsList.data || []);
        setFavMachines(FavMachineList.data || []);
        setFavRoutines(FavRoutineList.data || []);

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
    <div className="profile-container">
      <header className="profile-header">
          <h1>프로필</h1>
      </header>

      <div className="user-card">
        <div className="profile-icon">
          <span style={{fontSize: '30px'}}>👤</span>
        </div>
        <div className="user-info">
          <p>{currentUser.u_name}님</p>
          <p>{currentUser.email}</p>
          <p>가입일: {currentUser.signup_date?.split('T')[0]}</p>
        </div>
      </div>

      <div className="stats-container">
        <div className="stat-card">
          <span className="stat-label">총 운동일</span>
          <span className="stat-value">{exCount}일</span>
          </div>
      </div>

      <div className="menu-list">
        <div>
          {/* <div onClick={()=>favoriteClick()}>즐겨찾기</div>
            {openFavorite&&(
              <div>
                <div>
                  <div>헬스장</div>
                    {favGyms.length === 0 ? (
                        <div>즐겨찾기한 헬스장이 없습니다.</div>
                      ) : (
                        favGyms.map((gym, i) => (
                          <div key={gym.g_id || i}>
                            {gymNames[gym.g_id]}
                          </div>)))}
                </div>
                <div>
                  <div>운동기구</div>
                    {favMachines.length === 0 ? (
                      <div>즐겨찾기한 운동기구가 없습니다.</div>
                    ) : (
                      favMachines.map((machine, i) => (
                        <div key={machine.m_id || i}>{machine.m_name}</div>
                      )))}
                </div>

                <div>
                  <div>루틴</div>
                    {favRoutines.length === 0 ? (
                      <div>즐겨찾기한 루틴이 없습니다.</div>
                    ) : (
                      favRoutines.map((routine, i) => (
                        <div key={routine.r_id || i}>{routine.r_name}</div>
                      )))}
                </div>        
              </div>)} */}

          {/* <div>
              <div onClick={()=>boardClick()}>커뮤니티 기록</div>
              {openBoard&&(
                <div>
                  <div>내 게시글</div>
                  <div>내 댓글</div>
                </div>
              )}
          </div> */}
          <Link to="/note" className="menu-item">
            <div className="menu-title">✉️ 쪽지함</div>
          </Link>


          
          <div onClick={()=>profileEdit()} className="menu-title">
            <div className="menu-title">⚙️ 내 정보 관리</div>
          </div>
              {openEdit&&(
                <div>
                  <div><Link to="/profile/edit"><button>내 정보 수정</button></Link></div>
                  <div><button onClick={()=>userDelClick()}>탈퇴하기</button></div>
                </div>
              )}
          
      </div>
      <div>
        {userData.u_id!==1&&(
        <div>
          <Link to={"/note/create"} state={{ type: "admin", title: "관리자 문의사항" }}>
            <button>관리자 문의사항</button>
          </Link>
        </div>
        )}
      </div>
      <div>
        {userData.u_id==1&&(
        <div>
          <Link to={"/parts/create"}>
            <button>부위 추가</button>
          </Link>
        </div>)}
        </div>
        <div>
          <button onClick={logout}>로그아웃</button>
        </div>
      </div>
    </div>
  );
};

export default Profile;
