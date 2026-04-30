from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.models.gyms import Gym
from app.db.models.like_gyms import Like_Gym
from app.db.models.favorite_gyms import Favorite_Gym
from app.db.scheme.gyms import Gym_Create, Gym_Update


# CREATE
async def crud_gym_create(db: AsyncSession, data: Gym_Create):
    gym = Gym(**data.model_dump())
    db.add(gym)
    await db.flush()
    return gym


# DETAIL
async def crud_gym_get(db: AsyncSession, g_id: int):
    result = await db.execute(
        select(Gym).where(Gym.g_id == g_id)
    )
    return result.scalar_one_or_none()


# UPDATE
async def crud_gym_update(db: AsyncSession, gym: Gym, data: Gym_Update):
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(gym, k, v)
    await db.flush()
    return gym


# DELETE
async def crud_gym_delete(db: AsyncSession, gym: Gym):
    await db.delete(gym)
    await db.flush()


# LIST (🔥 ONLY DICT OUTPUT)
async def crud_gyms_gets(
    db: AsyncSession,
    skip: int,
    limit: int,
    name: str | None = None,
    address: str | None = None,
    sort: str | None = None
):

    like_sub = (
        select(
            Like_Gym.g_id.label("g_id"),
            func.count(Like_Gym.l_g_id).label("like_count")
        )
        .group_by(Like_Gym.g_id)
        .subquery()
    )

    fav_sub = (
        select(
            Favorite_Gym.g_id.label("g_id"),
            func.count(Favorite_Gym.f_g_id).label("favorite_count")
        )
        .group_by(Favorite_Gym.g_id)
        .subquery()
    )

    query = (
        select(
            Gym.g_id,
            Gym.g_name,
            Gym.g_addr,
            func.coalesce(like_sub.c.like_count, 0).label("like_count"),
            func.coalesce(fav_sub.c.favorite_count, 0).label("favorite_count")
        )
        .outerjoin(like_sub, Gym.g_id == like_sub.c.g_id)
        .outerjoin(fav_sub, Gym.g_id == fav_sub.c.g_id)
    )

    # filter
    if name:
        query = query.where(Gym.g_name.contains(name))
    if address:
        query = query.where(Gym.g_addr.contains(address))

    # SORT
    if sort == "g_name,asc":
        query = query.order_by(Gym.g_name.asc())
    elif sort == "g_name,desc":
        query = query.order_by(Gym.g_name.desc())
    elif sort == "g_id,asc":
        query = query.order_by(Gym.g_id.asc())
    elif sort == "g_id,desc":
        query = query.order_by(Gym.g_id.desc())
    elif sort == "like_count,desc":
        query = query.order_by(func.coalesce(like_sub.c.like_count, 0).desc())
    elif sort == "favorite_count,desc":
        query = query.order_by(func.coalesce(fav_sub.c.favorite_count, 0).desc())
    else:
        query = query.order_by(Gym.g_id.desc())

    # total
    count_query = select(func.count()).select_from(Gym)

    if name:
        count_query = count_query.where(Gym.g_name.contains(name))
    if address:
        count_query = count_query.where(Gym.g_addr.contains(address))

    total = (await db.execute(count_query)).scalar_one()

    result = await db.execute(query.offset(skip).limit(limit))

    return result.mappings().all(), total


# SEARCH
async def crud_gyms_search(db: AsyncSession, name: str | None, address: str | None):
    query = select(Gym)

    if name:
        query = query.where(Gym.g_name.contains(name))
    if address:
        query = query.where(Gym.g_addr.contains(address))

    result = await db.execute(query)
    return result.scalars().all()