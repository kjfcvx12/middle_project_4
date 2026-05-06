import React, { useEffect, useMemo, useState } from "react";
import {
    Search,
    MapPin,
    Heart,
    Phone,
    Clock,
    Pencil,
    Trash2,
    Plus
} from "lucide-react";

import "./Gym.css";
import {
    gyms_list,
    gyms_delete,
    gyms_toggle_like
} from "../../api/gyms.jsx";

import api from "../../api/api";
import { user_me } from "../../api/user.jsx";
import { useNavigate } from "react-router-dom";

export default function Gym() {
    const navigate = useNavigate();

    const [gyms, setGyms] = useState([]);
    const [query, setQuery] = useState("");
    const [sortKey, setSortKey] = useState("g_name");
    const [sortOption, setSortOption] = useState("like_count,desc");
    const [openId, setOpenId] = useState(null);
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState(null);

    useEffect(() => {
        loadMe();
    }, []);

    useEffect(() => {
        fetchGyms();
    }, [sortKey, sortOption]);

    const loadMe = async () => {
        try {
            await user_me();
            const profileRes = await api.get("/users/profile");
            setUser(profileRes.data);
        } catch (err) {
            console.error(err);
            setUser(null);
        }
    };

    const role = (
        user?.role ||
        user?.u_role ||
        user?.user_role ||
        ""
    ).toString().trim().toLowerCase();

    const isAdmin = role === "admin";

    const isStaff = [
        "admin",
        "staff",
        "manager",
        "trainer"
    ].includes(role);

    const fetchGyms = async () => {
        try {
            setLoading(true);

            let sortValue = "g_name,asc";

            if (sortKey === "g_id") sortValue = "g_id,desc";
            if (sortOption === "like_count,desc") sortValue = "like_count,desc";
            if (sortOption === "favorite_count,desc") sortValue = "favorite_count,desc";

            const res = await gyms_list({
                page: 1,
                size: 100,
                sort: sortValue,
                name: query || undefined
            });

            let data = [];

            if (Array.isArray(res?.data?.data)) data = res.data.data;
            else if (Array.isArray(res?.data)) data = res.data;

            setGyms(data);
        } catch (err) {
            console.error(err);
            setGyms([]);
        } finally {
            setLoading(false);
        }
    };

    const filtered = useMemo(() => gyms, [gyms]);

    const toggleOpen = (id) => {
        setOpenId(openId === id ? null : id);
    };

    const handleDelete = async (id) => {
        try {
            await gyms_delete(id);
            fetchGyms();
        } catch (err) {
            console.error(err);
        }
    };

    const handleLike = async (gym) => {
        try {
            await gyms_toggle_like(gym.g_id);

            setGyms((prev) =>
                prev.map((g) =>
                    g.g_id === gym.g_id
                        ? {
                            ...g,
                            like_yn: !g.like_yn,
                            like_count: g.like_yn
                                ? Math.max((g.like_count ?? 1) - 1, 0)
                                : (g.like_count ?? 0) + 1
                        }
                        : g
                )
            );
        } catch (err) {
            console.error(err);
        }
    };

    const isTrue = (v) =>
        v === true || v === 1 || v === "1" || v === "true";

    const getFacilities = (gym) => {
        const list = [];
        if (isTrue(gym.shower)) list.push("샤워실");
        if (isTrue(gym.parking)) list.push("주차장");
        if (isTrue(gym.elev)) list.push("엘리베이터");
        return list;
    };

    return (
        <div className="gym-page">
            <div className="gym-wrap">
                <div
                    style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center"
                    }}
                >
                    <h1 className="gym-title">헬스장 찾기</h1>

                    {isStaff && (
                        <button
                            className="detail-btn"
                            onClick={() => navigate("/gym/create")}
                        >
                            <Plus size={16} />
                            등록
                        </button>
                    )}
                </div>

                <div className="gym-search">
                    <Search size={20} />
                    <input
                        placeholder="헬스장 이름 검색"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === "Enter") fetchGyms();
                        }}
                    />
                </div>

                <div className="gym-sort-row">
                    <select
                        value={sortKey}
                        onChange={(e) => setSortKey(e.target.value)}
                    >
                        <option value="g_name">이름순</option>
                        <option value="g_id">등록순</option>
                    </select>

                    <select
                        value={sortOption}
                        onChange={(e) => setSortOption(e.target.value)}
                    >
                        <option value="like_count,desc">좋아요순</option>
                        <option value="favorite_count,desc">
                            즐겨찾기순
                        </option>
                    </select>
                </div>

                {!isStaff && (
                    <div style={{ marginBottom: "12px", color: "#999" }}>
                        현재 권한: 일반회원
                    </div>
                )}

                {loading ? (
                    <div className="gym-loading">불러오는 중...</div>
                ) : filtered.length === 0 ? (
                    <div className="gym-loading">검색 결과 없음</div>
                ) : (
                    filtered.map((gym) => {
                        const opened = openId === gym.g_id;
                        const facilities = getFacilities(gym);

                        return (
                            <div className="gym-card" key={gym.g_id}>
                                <div className="gym-card-top">
                                    <div className="gym-left">
                                        <h2>{gym.g_name}</h2>

                                        <p className="gym-address">
                                            <MapPin size={16} />
                                            {gym.g_addr}
                                        </p>

                                        <div className="gym-meta">
                                            <span className="likes">
                                                <Heart
                                                    size={15}
                                                    fill={
                                                        gym.like_yn
                                                            ? "#ff4d6d"
                                                            : "none"
                                                    }
                                                    color={
                                                        gym.like_yn
                                                            ? "#ff4d6d"
                                                            : "#8e93aa"
                                                    }
                                                />
                                                {gym.like_count ?? 0}
                                            </span>

                                            <span className="likes">
                                                ⭐ {gym.favorite_count ?? 0}
                                            </span>
                                        </div>

                                        <button
                                            className="detail-btn"
                                            onClick={() =>
                                                toggleOpen(gym.g_id)
                                            }
                                        >
                                            {opened ? "접기" : "상세보기"}
                                        </button>
                                    </div>

                                    <div className="gym-actions">
                                        {isStaff && (
                                            <button
                                                className="icon-btn"
                                                onClick={() =>
                                                    navigate(`/gym/edit/${gym.g_id}`)
                                                }
                                            >
                                                <Pencil size={16} />
                                            </button>
                                        )}

                                        {isAdmin && (
                                            <button
                                                className="icon-btn danger"
                                                onClick={() =>
                                                    handleDelete(gym.g_id)
                                                }
                                            >
                                                <Trash2 size={16} />
                                            </button>
                                        )}
                                    </div>

                                    <Heart
                                        size={34}
                                        className={`card-heart ${gym.like_yn ? "liked" : ""
                                            }`}
                                        fill={
                                            gym.like_yn
                                                ? "#ff4d6d"
                                                : "rgba(0,0,0,0.15)"
                                        }
                                        color={
                                            gym.like_yn
                                                ? "#ff4d6d"
                                                : "#ffffff"
                                        }
                                        strokeWidth={2.3}
                                        onClick={() => handleLike(gym)}
                                    />
                                </div>

                                {opened && (
                                    <div className="gym-detail">
                                        <div className="detail-row">
                                            <Phone size={17} />
                                            {gym.g_tel}
                                        </div>

                                        <div className="detail-row">
                                            <Clock size={17} />
                                            {gym.open_time}
                                        </div>

                                        <h3>시설</h3>

                                        <div className="facility-wrap">
                                            {facilities.length > 0 ? (
                                                facilities.map((item, idx) => (
                                                    <span
                                                        key={idx}
                                                        className="facility-chip"
                                                    >
                                                        {item}
                                                    </span>
                                                ))
                                            ) : (
                                                <span className="facility-none">
                                                    시설 정보 없음
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                )}
                            </div>
                        );
                    })
                )}
                <button onClick={()=>navigate("/machines")}>
                    운동기구 목록 보기
                </button>
            </div>
        </div>
    );
}
