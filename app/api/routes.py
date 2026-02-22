from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.database_async import get_async_db
from app.models.schemas import User
from app.services.matching_service import matching_service
from app.services.cache_service import cache_service

router = APIRouter(prefix="/api", tags=["matches"])

@router.post("/matches/{user_id}")
async def find_matches(
    user_id: str,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_db)
):
    """Find best matches for a user (ASYNC VERSION)"""
    cache_key= f"matches:{user_id}:{limit}"
    cached_result = cache_service.get(cache_key)
    if cached_result:
        print("Cache hit for", user_id)
        return cached_result
    # Get the user (async)
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get all other users (async)
    result = await db.execute(select(User).filter(User.id != user_id))
    other_users = result.scalars().all()
    
    # Calculate matches (this part is still sync, but fast)
    matches = []
    for other_user in other_users:
        result = matching_service.calculate_match_score(
            my_skills_want=user.skillsWant or [],
            my_skills_have=user.skillsHave or [],
            their_skills_have=other_user.skillsHave or [],
            their_skills_want=other_user.skillsWant or []
        )
        
        if result["score"] > 0:
            matches.append({
                "user_id": other_user.id,
                "username": other_user.username,
                "email": other_user.email,
                "score": result["score"],
                "what_i_get": result["what_i_get"],
                "what_i_give": result["what_i_give"]
            })
    
    matches.sort(key=lambda x: x["score"], reverse=True)
    
    response = {
        "user_id": user_id,
        "username": user.username,
        "total_matches": len(matches),
        "matches": matches[:limit]
    }
    cache_service.set(cache_key, response, ttl=300)
    return response