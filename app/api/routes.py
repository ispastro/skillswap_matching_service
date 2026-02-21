from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.models.database import SessionLocal
from app.models.schemas import User
from app.services.matching_service import matching_service

router = APIRouter(prefix="/api", tags=["matches"])

@router.post("/matches/{user_id}")
def find_matches(user_id: str, limit: int = 10):
    """
    Find best matches for a user
    
    Args:
        user_id: User ID to find matches for
        limit: Maximum number of matches to return (default 10)
    
    Returns:
        List of matches with scores
    """
    db = SessionLocal()
    try:
        # Get the user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get all other users
        other_users = db.query(User).filter(User.id != user_id).all()
        
        # Calculate matches
        matches = []
        for other_user in other_users:
            result = matching_service.calculate_match_score(
                my_skills_want=user.skillsWant or [],
                my_skills_have=user.skillsHave or [],
                their_skills_have=other_user.skillsHave or [],
                their_skills_want=other_user.skillsWant or []
            )
            
            # Only include if score > 0
            if result["score"] > 0:
                matches.append({
                    "user_id": other_user.id,
                    "username": other_user.username,
                    "email": other_user.email,
                    "score": result["score"],
                    "what_i_get": result["what_i_get"],
                    "what_i_give": result["what_i_give"]
                })
        
        # Sort by score (highest first)
        matches.sort(key=lambda x: x["score"], reverse=True)
        
        # Return top N matches
        return {
            "user_id": user_id,
            "username": user.username,
            "total_matches": len(matches),
            "matches": matches[:limit]
        }
        
    finally:
        db.close()
