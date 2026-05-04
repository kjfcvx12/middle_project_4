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
import { gyms_list, gyms_create, gyms_update, gyms_delete } from "../../api/gyms.jsx";
import { user_me } from "../../api/user.jsx";

export default function Gym() {
    const [gyms, setGyms] = useState([]);
    const [query, setQuery] = useState("");
    const [sortKey, setSortKey] = useState("g_name");
    const [sortOption, setSortOption] = useState("distance");
    const [openId, setOpenId] = useState(null);
    const [loading, setLoading] = useState(true);

    const [isAdmin, setIsAdmin] = useState(false);
    const [isStaff, setIsStaff] = useState(false);

    useEffect(() => {
        fetchUser();
        fetchGyms();
    }, [sortKey, sortOption]);

    const fetchUser = async () => {
        try {
            const res = await user_me();
            const role = res.data.role;

            setIsAdmin(role === "admin");
            setIsStaff(role === "admin" || role === "staff");
        } catch {
            setIsAdmin(false);
            setIsStaff(false);
        }
    };

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
            console.error("헬스장 불러오기 실패", err);
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

    const handleCreate = () => {
        alert("헬스장 생성 모달 연결 예정");
    };

    const handleEdit = (gym) => {
        alert(`${gym.g_name} 수정 모달 연결 예정`);
    };

    const handleDelete = async (id) => {
        if (!window.confirm("정말 삭제하시겠습니까?")) return;

        try {
            await gyms_delete(id);
            fetchGyms();
        } catch {
            alert("삭제 실패");
        }
    };

    const isTrue = (value) =>
        value === true || value === 1 || value === "1" || value === "true";

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

                {/* ✅ 관리자 생성 버튼 (우측 영역) */}
                {isAdmin && (
                    <div style={{ textAlign: "right", marginBottom: "10px" }}>
                        <button onClick={handleCreate}>
                            <Plus size={16} />
                            생성
                        </button>
                    </div>
                )}

                {/* 검색 */}
                <div className="gym-search">
                    <Search size={20} />
                    <input
                        type="text"
                        placeholder="헬스장 이름 / 주소 검색"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                </div>

                {/* 정렬 */}
                <div className="gym-sort-row">
                    <select
                        value={sortKey}
                        onChange={(e) => setSortKey(e.target.value)}
                    >
                        <option value="g_name">이름순</option>
                        <option value="g_addr">주소순</option>
                        <option value="g_id">등록순</option>
                    </select>

                    <select
                        value={sortOption}
                        onChange={(e) => setSortOption(e.target.value)}
                    >
                        <option value="distance">거리순</option>
                        <option value="rating">별점순</option>
                        <option value="review">리뷰순</option>
                    </select>
                </div>

                {/* 목록 */}
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

                                    {/* 카드 우측 버튼 영역 */}
                                    <Heart className="card-heart" size={34} />

                                    {(isAdmin || isStaff) && (
                                        <div style={{ display: "flex", gap: "6px" }}>

                                            {(isAdmin || isStaff) && (
                                                <button onClick={() => handleEdit(gym)}>
                                                    <Pencil size={16} />
                                                </button>
                                            )}

                                            {isAdmin && (
                                                <button onClick={() => handleDelete(gym.g_id)}>
                                                    <Trash2 size={16} />
                                                </button>
                                            )}

                                        </div>
                                    )}
                                </div>

                                {/* 상세 */}
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