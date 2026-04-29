import { useState } from "react";
import { useAuth } from "../AuthContext";

const Login = () => {
  const { login, logout, signup } = useAuth();

  const [isOpen, setIsOpen] = useState(true);
  const [loginData, setLoginData] = useState({
    email: "",
    pw: "",
    autologin: false,
  });
  const [signupData, setSignupData] = useState({
    email: "",
    pw: "",
    u_name: "",
    phone: "",
    info: "",
  });

  // 입력값 변경 핸들러
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    const finalValue = type === "checkbox" ? checked : value;

    if (isOpen) {
      setLoginData({ ...loginData, [name]: value });
    } else {
      setSignupData({ ...signupData, [name]: value });
    }
  };

  // 로그인 처리
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (isOpen) {
      // 로그인 로직
      const result = await login(loginData);
      if (result.success) {
        alert(`환영합니다!`);
      } else {
        alert(result.error || "로그인에 실패했습니다.");
      }
    } else {
      // 회원가입 로직
      const result = await signup(signupData);
      if (result.success) {
        alert("회원가입이 완료되었습니다. 로그인해 주세요.");
        setIsOpen(true);
      } else {
        alert(result.error || "회원가입 실패");
      }
    }
  };

  return (
    <div style={{ padding: "50px", textAlign: "center" }}>
      {isOpen && (
        <div>
          <div>
            <h2>로그인</h2>
            <form onSubmit={handleSubmit} style={formStyle}>
              <input
                name="email"
                placeholder="email"
                value={loginData.email}
                onChange={handleChange}
                required
              />
              <input
                name="pw"
                type="password"
                placeholder="비밀번호"
                value={loginData.pw}
                onChange={handleChange}
                required
              />
              <input
                type="checkbox"
                id="autologin"
                name="autologin"
                checked={loginData.autologin}
                onChange={handleChange}
              />
              <label htmlFor="autologin">로그인 상태 유지</label>

              {/* Silent Refresh 사용법 */}
              <button type="submit">로그인</button>
            </form>
            <button>아이디 찾기</button>
            <button>비밀번호 찾기</button>
            <button onClick={() => setIsOpen(false)}>회원가입</button>
          </div>
        </div>
      )}

      {!isOpen && (
        <div>
          <div>
            <h2>회원가입</h2>
            <form onSubmit={handleSubmit} style={formStyle}>
              <input
                name="email"
                type="email"
                placeholder="email"
                value={signupData.email}
                onChange={handleChange}
                required
              />
              <input
                name="pw"
                type="password"
                placeholder="비밀번호"
                value={signupData.pw}
                onChange={handleChange}
                required
              />
              <input
                name="u_name"
                type="text"
                placeholder="이름"
                value={signupData.u_name}
                onChange={handleChange}
                required
              />
              <input
                name="phone"
                type="text"
                placeholder="전화번호"
                value={signupData.phone}
                onChange={handleChange}
                required
              />
              <input
                name="info"
                type="text"
                placeholder="자기소개"
                value={signupData.info}
                onChange={handleChange}
                required
              />
              <button type="submit">회원가입</button>
            </form>
            <button onClick={() => setIsOpen(true)}>로그인</button>
          </div>
        </div>
      )}
    </div>
  );
};

const formStyle = { display: "flex", flexDirection: "column", gap: "10px" };

export default Login;
