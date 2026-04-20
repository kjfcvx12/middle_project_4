from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.scheme.gyms import GymCreate, GymUpdate, GymResponse, GymListItem
from app.services import gyms as gym_service

router = APIRouter(prefix="/gyms", tags=["Gyms"])

# 헬스장 등록
@router.post("")
def createGym(
    data: GymCreate, 
    db: Session = Depends(get_db),
    # 관리자 권한 체크 코드 추가 필요
):
    try:
        gym = gym_service.createGymService(db, data)

        return {
            "msg": "헬스장 등록 완료",
            "g_id": gym.g_id
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=400,
        )

# 헬스장 목록 조회
@router.get("")
def listGyms(
    page: int = 1,
    size: int = 10,
    sort: str | None = None,
    name: str | None = None,
    address: str | None = None,
    db: Session = Depends(get_db),
):
    skip = (page - 1) * size

    gyms, total = gym_service.listGymService(
        db=db,
        skip=skip,
        limit=size,
        name=name,
        address=address,
        sort=sort
    )
    if not gyms:
        raise HTTPException(
            status_code=404
        )

    data = [
        {
            "g_id": g.g_id,
            "g_name": g.g_name,
            "g_addr": g.g_addr,
            "like_count": getattr(g, "like_count", 0),
            "favorite_count": getattr(g, "favorite_count", 0),
        }
        for g in gyms
    ]

    return {
        "total": total,
        "page": page,
        "size": size,
        "data": data,
    }

# 헬스장 상세 조회
@router.get("/{g_id}", response_model=GymResponse)
def gymDetail(
    g_id: int,
    db: Session = Depends(get_db),
):
    gym = gym_service.getGymService(db, g_id)

    if not gym:
        raise HTTPException(
            status_code=404
        )

    return gym

# 헬스장 정보 수정
@router.put("/{g_id}")
def updateGym(
    g_id: int,
    data: GymUpdate,
    db: Session = Depends(get_db),
    # user=Depends(get_manager_or_admin)  # 임시... 권한 추가하고 수정해야 함 (매니저 / 관리자)
):
    gym = gym_service.updateGymService(db, g_id, data)

    # 명세서에서는 실패 시 error 400
    # 400은 클라이언트가 보낸 요청 자체가 잘못된 것이고, 
    # 404는 요청은 정상인데 대상이 존재하지 않는 것이라 404가 더 정확하다고 함
    if gym is None:
        raise HTTPException(
            status_code=404
        )

    return {
        "msg": "수정 완료"
    }

# 헬스장 삭제
@router.delete("/{g_id}")
def deleteGym(
    g_id: int,
    db: Session = Depends(get_db),
    # user=Depends(get_admin_user)  # 임시... 권한 추가하고 수정해야 함 (관리자)
):
    success = gym_service.deleteGymService(db, g_id)

    # 명세서에서는 실패 시 error 500
    # 500은 서버가 처리 못한 내부 오류고
    # 404은 삭제할 대상이 없는 것이라 404가 더 정확하다고 함
    if success is False:
        raise HTTPException(
            status_code=404
        )

    return {
        "msg": "헬스장 삭제 완료"
    }

# 헬스장 소속 트레이너 조회
@router.get("/{g_id}/staff")
def getGymStaff(
    g_id: int,
    db: Session = Depends(get_db),
):
    data = gym_service.getGymTrainerService(db, g_id)

    return {
        "data": [
            {
                "u_id": d.u_id,
                "u_name": d.u_name
            }
            for d in data
        ]
    }

# 헬스장 운동기구 목록 조회
@router.get("/machines/{g_id}")
def getGymMachines(
    g_id: int,
    db: Session = Depends(get_db),
):
    data = gym_service.getGymMachinesService(db, g_id)

    return {
        "data": [
            {
                "m_id": d.m_id,
                "m_name": d.m_name,
                "qty": d.qty
            }
            for d in data
        ]
    }