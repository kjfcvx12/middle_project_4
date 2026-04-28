import React from 'react';
import { useAuth } from '../AuthContext';


const Profile = () => {
    const {setIsLoggedIn} =useAuth();
    return (
        <div>
            <button onClick={()=>{setIsLoggedIn(false)}}>로그아웃</button>
        </div>
    );
};

export default Profile;
