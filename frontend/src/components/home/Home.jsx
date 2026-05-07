import React from 'react';
import fitChickLogo from '../../image/FitChick.png';

const Home = () => {
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
            </div>
        </div>
    );
};

export default Home;
