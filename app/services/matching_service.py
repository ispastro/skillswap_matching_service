from typing import List, Dict
import numpy as np
from app.services.embedding_service import embedding_service

class MatchingService:
    def calculate_match_score(
        self,
        my_skills_want: List[str],
        my_skills_have: List[str],
        their_skills_have: List[str],
        their_skills_want: List[str]
    ) -> Dict:
        """Calculate match score between two users"""
        
        # Stage 1: Exact matches
        what_i_get = self._find_exact_matches(my_skills_want, their_skills_have)
        what_i_give = self._find_exact_matches(their_skills_want, my_skills_have)
        
        # Calculate score (0-100)
        score = self._calculate_score(
            len(what_i_get),
            len(what_i_give),
            len(my_skills_want),
            len(their_skills_want)
        )
        
        return {
            "score": round(score, 2),
            "what_i_get": what_i_get,
            "what_i_give": what_i_give
        }
    
    def _find_exact_matches(self, want: List[str], have: List[str]) -> List[str]:
        """Find exact matches (case-insensitive)"""
        want_lower = [s.lower() for s in want]
        have_lower = [s.lower() for s in have]
        
        matches = []
        for skill in want:
            if skill.lower() in have_lower:
                matches.append(skill)
        
        return matches
    
    def _calculate_score(
        self,
        i_get_count: int,
        i_give_count: int,
        i_want_count: int,
        they_want_count: int
    ) -> float:
        """Calculate match score (0-100)"""
        
        if i_want_count == 0 and they_want_count == 0:
            return 0.0
        
        # What I get (60% weight)
        get_score = (i_get_count / i_want_count * 60) if i_want_count > 0 else 0
        
        # What I give (40% weight)
        give_score = (i_give_count / they_want_count * 40) if they_want_count > 0 else 0
        
        return get_score + give_score

# Singleton
matching_service = MatchingService()
