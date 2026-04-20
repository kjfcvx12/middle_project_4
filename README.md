# 🏋️ Fitness Management API

헬스 초보자를 위한 운동 관리 백엔드 API입니다.  
운동 기록(Log)과 즐겨찾기(Favorites) 기능을 중심으로 설계되었습니다.

---

## 주요 기능

### Favorites (즐겨찾기)
- 헬스장 / 운동기구 / 루틴 즐겨찾기
- Toggle 방식 (추가/삭제 통합)
- 중복 방지 (UniqueConstraint)
- Cascade 삭제 지원

---

### Logs (운동 기록)
- 운동 기록 생성 (Log + LogDetail)
- 사용자별 기록 조회
- 기록 삭제 시 상세 자동 삭제

---

## 프로젝트 구조


app/
├─ db/
│ ├─ models/
│ │ ├─ logs.py
│ │ ├─ log_details.py
│ │ └─ favorites_.py
│ ├─ crud/
│ │ ├─ logs.py
│ │ ├─ log_details.py
│ │ └─ favorites_.py
│
├─ services/
│ ├─ logs.py
│ └─ favorites.py
│
├─ routers/
│ ├─ logs.py
│ └─ favorites.py
│
├─ schemas/
│ ├─ log.py
│ └─ log_detail.py


---

## 기술 스택

- FastAPI  
- SQLAlchemy (ORM)  
- Pydantic  
- JWT Authentication  

---

## 핵심 설계

### 1. 계층 분리 구조


Router → Service → CRUD → Model


| 계층 | 역할 |
|------|------|
| Router | API 엔드포인트 |
| Service | 비즈니스 로직 |
| CRUD | DB 처리 |
| Model | 테이블 정의 |

---

### 2. Toggle 기반 즐겨찾기

```python
if fav:
    db.delete(fav)
else:
    db.add(new_fav)
API 단순화
프론트 상태 관리 용이
3. Log + LogDetail 구조
User
 └── Log
      └── LogDetail
Log: 운동 단위 기록
LogDetail: 세트 / 반복 상세
4. Cascade 설계
ForeignKey(..., ondelete="CASCADE")
relationship(cascade="all, delete-orphan")
동작
유저 삭제 → 로그 삭제 → 로그 상세 삭제
로그 삭제 → 로그 상세 자동 삭제
헬스장 삭제 → 즐겨찾기 자동 삭제
5. 트랜잭션 처리
db.flush()   # PK 확보
db.commit()  # 최종 저장

API 명세


Logs

Method	Endpoint	설명
POST	/logs	운동 기록 생성
GET	/logs	내 기록 조회
DELETE	/logs/{log_id}	기록 삭제


Favorites

Method	Endpoint	설명
GET	/favorites/gym	헬스장 즐겨찾기 조회
POST	/favorites/gym/{id}/toggle	즐겨찾기 토글
DELETE	/favorites/gym/{id}	즐겨찾기 삭제

※ machine / routine 동일 구조

 예시 요청
 
로그 생성
{
  "r_id": 1,
  "m_id": 2,
  "attend": true,
  "details": [
    {
      "sets": 3,
      "reps": 10,
      "memo": "good",
      "fail_memo": null
    }
  ]
}

 설계 장점
단순한 API 구조 (toggle)
높은 데이터 무결성 (cascade)
유지보수 용이 (계층 분리)
확장 가능 (통계 / 추천 기능)


 개선 사항
Pagination 미적용
Response Schema 부족
N+1 문제 가능성
권한 처리 고도화 필요


 배운 점
ORM 관계 설계
Cascade를 통한 데이터 정합성 유지
Service 계층 분리의 중요성
트랜잭션 처리 방식


 담당 기능
Favorites 시스템 구현
Logs / LogDetail 설계 및 구현
Cascade 구조 설계