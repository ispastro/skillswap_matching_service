from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.database_async import get_async_db
from app.models.schemas import User
from app.services.matching_service import matching_service
from app.services.cache_service import cache_service
from app.api.models import MatchResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["matches"])

@router.post("/matches/{user_id}", response_model=MatchResponse)
async def find_matches(
    user_id: str,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_db)
):
    """Find best matches for a user (ASYNC VERSION)"""
    try:
        # Validate limit
        if limit < 1 or limit > 100:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
        
        # Check cache
        cache_key = f"matches:{user_id}:{limit}"
        cached_result = cache_service.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit for user {user_id}")
            return cached_result
        
        # Get the user (async)
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        
        # Get all other users (async)
        result = await db.execute(select(User).filter(User.id != user_id))
        other_users = result.scalars().all()
        
        # Calculate matches
        matches = []
        for other_user in other_users:
            try:
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
            except Exception as e:
                logger.error(f"Error calculating match for user {other_user.id}: {e}")
                continue
        
        matches.sort(key=lambda x: x["score"], reverse=True)
        
        response = {
            "user_id": user_id,
            "username": user.username,
            "total_matches": len(matches),
            "matches": matches[:limit]
        }
        
        # Cache result
        cache_service.set(cache_key, response, ttl=300)
        logger.info(f"Found {len(matches)} matches for user {user_id}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in find_matches: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")