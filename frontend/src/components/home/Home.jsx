import React, { useEffect, useState } from 'react';
import fitChickLogo from '../../image/FitChick.png';
import ad1 from '../../image/ad1.jpg'
import ad2 from '../../image/ad2.jpg'
import { getLogs } from '../../api/logApi';

const Home = () => {
    const [exCount, setExCount]= useState(0);

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


    return (
        <div style={{
              display: 'flex',          // 플렉스 박스 활성화
              justifyContent: 'center', // 가로 방향 가운데 정렬
              alignItems: 'center',     // 세로 방향 가운데 정렬 (필요 시)
              width: '100%',            // 전체 너비 차지
              margin: '20px 0'          // 위아래 여유 공간
          }}>
            <div style={{
                backgroundColor: '#1E1E1E',   // 카드 배경색 (다크)
                borderRadius: '16px',         // 둥근 모서리
                padding: '10px 5px',         // 안쪽 여백 (상하, 좌우)
                textAlign: 'center',          // 텍스트 중앙 정렬
                boxShadow: '0 8px 16px rgba(0,0,0,0.5)' // 입체감 있는 그림자
            }}>
                <p style={{
                    color: 'black',
                    fontSize: '40px',
                    fontWeight: 'bold',
                    WebkitTextStroke: '1px yellow',
                    textAlign: "center"
                    }}>
                        FitChick
                </p>
                <img src={fitChickLogo} style={{ 
                    maxWidth: "20%", 
                    height: "auto", 
                    display: "block", 
                    margin: "0 auto", // 상하 마진은 0, 좌우는 중앙 정렬
                    verticalAlign: "middle" }}></img>

                <div style={{ 
                    color: '#A0A0A0',         // '총 운동일' 글자색 (회색)
                    fontSize: '15px', 
                    marginBottom: '10px',
                    letterSpacing: '-0.5px'
                }}>
                    <h2>총 운동일</h2>
                </div>
                <div style={{ 
                    color: '#FF6B35',         // 숫자 강조색 (오렌지)
                    fontSize: '32px',         // 숫자 크게
                    fontWeight: '800'         // 아주 굵게
                }}>
                    {exCount}
                    <span style={{ fontSize: '20px', marginLeft: '4px', color: '#FFFFFF' }}>일</span>
                </div>
                <br></br>
                <div style={{ 
                    display: "flex", 
                    justifyContent: "center", // 중앙 정렬 (왼쪽 정렬 원하면 생략)
                    gap: "10px"               // 이미지 사이 간격
                }}>
                    <img src={ad1} style={{ 
                        width: "10%",         // 고정 비율로 크기 조절
                        height: "auto", 
                        display: "block" 
                    }} alt="ad1" />
                    
                    <img src={ad2} style={{ 
                        width: "10%",         // 첫 번째 이미지와 동일한 너비
                        height: "auto", 
                        display: "block" 
                    }} alt="ad2" />
                </div>
            </div>
        </div>
    );
};

export default Home;
