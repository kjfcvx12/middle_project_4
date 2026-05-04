import React, { useEffect, useMemo, useState } from "react";
import {
    Search,
    MapPin,
    Heart,
    Star,
    ChevronDown,
    ChevronUp,
    Phone,
    Clock,
    Plus,
    Pencil,
    Trash2
} from "lucide-react";

import "./Gym.css";
import { gyms_list, gyms_delete, gyms_toggle_like } from "../../api/gyms.jsx";
import { useNavigate } from "react-router-dom";

export default function Gym() {
    const navigate = useNavigate();

    const [gyms, setGyms] = useState([]);
    const [query, setQuery] = useState("");
    const [sortKey, setSortKey] = useState("g_name");
    const [sortOption, setSortOption] = useState("distance");
    const [openId, setOpenId] = useState(null);
    const [loading, setLoading] = useState(true);

    const [user, setUser] = useState(null);

    const role = user?.role;
    const isAdmin = role === "admin";
    const isStaff = role === "admin" || role === "staff";

    useEffect(() => {
        const saved = localStorage.getItem("user");
        setUser(saved ? JSON.parse(saved) : null);
    }, []);

    useEffect(() => {
        fetchGyms();
    }, [sortKey, sortOption]);

    const fetchGyms = async () => {
        try {
            setLoading(true);

            const res = await gyms_list({
                page: 1,
                size: 100,
                sort: `${sortKey},asc`,
            });

            let data = [];

            if (Array.isArray(res?.data)) data = res.data;
            else if (Array.isArray(res?.data?.data)) data = res.data.data;

            data = data.map((gym, index) => ({
                ...gym,
                rating: 4.2 + (index % 5) * 0.15,
                review_count: 35 + index * 28,
                distance: 0.8 + index * 0.7,
            }));

            if (sortOption === "distance") {
                data.sort((a, b) => a.distance - b.distance);
            } else if (sortOption === "rating") {
                data.sort((a, b) => b.rating - a.rating);
            } else if (sortOption === "review") {
                data.sort((a, b) => b.review_count - a.review_count);
            }

            setGyms(data);
        } catch (err) {
            console.error(err);
            setGyms([]);
        } finally {
            setLoading(false);
        }
    };

    const filtered = useMemo(() => {
        return gyms.filter((gym) =>
            `${gym.g_name || ""} ${gym.g_addr || ""}`
                .toLowerCase()
                .includes(query.toLowerCase())
        );
    }, [gyms, query]);

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

    // 🔥 핵심 수정 (좋아요 동기화)
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
                                ? (g.like_count ?? 1) - 1
                                : (g.like_count ?? 0) + 1,
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

                <h1 className="gym-title">헬스장 찾기</h1>

                <div className="gym-search">
                    <Search size={20} />
                    <input
                        placeholder="헬스장 이름 / 주소 검색"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                </div>

                <div className="gym-sort-row">
                    <select value={sortKey} onChange={(e) => setSortKey(e.target.value)}>
                        <option value="g_name">이름순</option>
                        <option value="g_addr">주소순</option>
                        <option value="g_id">등록순</option>
                    </select>

                    <select value={sortOption} onChange={(e) => setSortOption(e.target.value)}>
                        <option value="distance">거리순</option>
                        <option value="rating">별점순</option>
                        <option value="review">리뷰순</option>
                    </select>
                </div>

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
                                            <span className="rating">
                                                <Star size={15} fill="currentColor" />
                                                {gym.rating.toFixed(1)}
                                            </span>

                                            <span className="likes">
                                                <Heart size={15} />
                                                {gym.like_count ?? 0}
                                            </span>

                                            <span>
                                                {gym.distance.toFixed(1)}km
                                            </span>
                                        </div>

                                        <button
                                            className="detail-btn"
                                            onClick={() => toggleOpen(gym.g_id)}
                                        >
                                            {opened ? "접기" : "상세보기"}
                                            {opened ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                                        </button>
                                    </div>

                                    {/* 수정/삭제 유지 */}
                                    <div className="gym-actions">
                                        {isStaff && (
                                            <button
                                                className="icon-btn"
                                                onClick={() => navigate(`/gym/edit/${gym.g_id}`)}
                                            >
                                                <Pencil size={16} />
                                            </button>
                                        )}

                                        {isAdmin && (
                                            <button
                                                className="icon-btn danger"
                                                onClick={() => handleDelete(gym.g_id)}
                                            >
                                                <Trash2 size={16} />
                                            </button>
                                        )}
                                    </div>

                                    {/* 🔥 하트 수정 핵심 */}
                                    <Heart
                                        className="card-heart"
                                        size={34}
                                        onClick={() => handleLike(gym)}
                                        fill={gym.like_yn ? "#ff4d6d" : "none"}
                                        stroke={gym.like_yn ? "#ff4d6d" : "#8e93aa"}
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
                                                    <span key={idx} className="facility-chip">
                                                        {item}
                                                    </span>
                                                ))
                                            ) : (
                                                <span className="facility-none">
                                                    시설 정보 없음
                                                </span>
                                            )}
                                        </div>

                                        <div className="detail-bottom">
                                            리뷰 {gym.review_count}개 | 즐겨찾기 {gym.favorite_count ?? 0}명
                                        </div>
                                    </div>
                                )}

                            </div>
                        );
                    })
                )}
            </div>
        </div>
    );
}