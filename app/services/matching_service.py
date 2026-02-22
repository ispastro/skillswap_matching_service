from typing import List, Dict
import numpy as np
from app.services.embedding_service import embedding_service

class MatchingService:
    def __init__(self):
        self.semantic_threshold = 0.5  # 50% similarity minimum
    
    def calculate_match_score(
        self,
        my_skills_want: List[str],
        my_skills_have: List[str],
        their_skills_have: List[str],
        their_skills_want: List[str]
    ) -> Dict:
        """Calculate match score with exact + semantic matching"""
        
        exact_i_get = self._find_exact_matches(my_skills_want, their_skills_have)
        exact_i_give = self._find_exact_matches(their_skills_want, my_skills_have)
        
        remaining_i_want = [s for s in my_skills_want if s not in exact_i_get]
        remaining_they_have = [s for s in their_skills_have if s.lower() not in [x.lower() for x in exact_i_get]]
        
        semantic_i_get = self._find_semantic_matches(remaining_i_want, remaining_they_have)
        
        remaining_they_want = [s for s in their_skills_want if s not in exact_i_give]
        remaining_i_have = [s for s in my_skills_have if s.lower() not in [x.lower() for x in exact_i_give]]
        
        semantic_i_give = self._find_semantic_matches(remaining_they_want, remaining_i_have)
        
        all_i_get = exact_i_get + [m["skill"] for m in semantic_i_get]
        all_i_give = exact_i_give + [m["skill"] for m in semantic_i_give]
        
        score = self._calculate_score(
            len(all_i_get),
            len(all_i_give),
            len(my_skills_want),
            len(their_skills_want)
        )
        
        return {
            "score": round(score, 2),
            "what_i_get": {
                "exact": exact_i_get,
                "semantic": semantic_i_get
            },
            "what_i_give": {
                "exact": exact_i_give,
                "semantic": semantic_i_give
            }
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
    
    def _find_semantic_matches(self, want: List[str], have: List[str]) -> List[Dict]:
        """Find semantic matches using AI embeddings"""
        if not want or not have:
            return []
        
        matches = []
        
        # Generate embeddings for all skills
        want_embeddings = embedding_service.generate_embeddings_batch(want)
        have_embeddings = embedding_service.generate_embeddings_batch(have)
        
        for i, want_skill in enumerate(want):
            best_match = None
            best_similarity = 0
            
            for j, have_skill in enumerate(have):
                similarity = self._cosine_similarity(want_embeddings[i], have_embeddings[j])
                
                if similarity > best_similarity and similarity >= self.semantic_threshold:
                    best_similarity = similarity
                    best_match = have_skill
            
            if best_match:
                matches.append({
                    "skill": want_skill,
                    "matched_with": best_match,
                    "similarity": round(float(best_similarity), 2)
                })
        
        return matches
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
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
