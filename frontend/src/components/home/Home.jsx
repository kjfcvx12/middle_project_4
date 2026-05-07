import React, { useEffect, useState } from 'react';
import fitChickLogo from '../../image/FitChick.png';
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
        <div>
            <h1>Home</h1>
            <div>
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
                    maxWidth: "40%", 
                    height: "auto", 
                    display: "block", 
                    margin: "0 auto" }}></img>


                    <div>
                        <div> 총 운동일</div>
                        <div>{exCount}일</div>
                    </div>
            </div>
        </div>
    );
};

export default Home;
