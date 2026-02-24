from pydantic import BaseModel, Field
from typing import List, Optional

class SemanticMatch(BaseModel):
    skill: str
    matched_with: str
    similarity: float

class MatchDetails(BaseModel):
    exact: List[str]
    semantic: List[SemanticMatch]

class UserMatch(BaseModel):
    user_id: str
    username: str
    email: str
    score: float
    what_i_get: MatchDetails
    what_i_give: MatchDetails

class MatchResponse(BaseModel):
    user_id: str
    username: str
    total_matches: int
    matches: List[UserMatch]

class HealthResponse(BaseModel):
    status: str
    service_name: str
    port: int
    database_connected: bool = Field(default=False)
    redis_connected: bool = Field(default=False)
    model_loaded: bool = Field(default=False)
