import React from 'react';
import { useAuth } from '../AuthContext';

const Profile = () => {
    const {logout} =useAuth();
    return (
        <div>
            <button onClick={logout}>로그아웃</button>
        </div>
    );
};

export default Profile;
