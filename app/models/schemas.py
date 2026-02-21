from sqlalchemy import Column, String, Text, ARRAY, DateTime
from pgvector.sqlalchemy import Vector

from app.models.database  import Base

class User(Base):
    __tablename__="User"
    id =Column(Text, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    bio = Column(Text)
    skillsWant =Column(ARRAY(Text))
    skillsHave= Column(ARRAY(Text))
    normalizedSkillsHave = Column(ARRAY(Text))
    normalizedSkillsWant = Column(ARRAY(Text))
    createdAt =Column(DateTime)
    updatedAt = Column(DateTime)
   
class SkillEmbedding(Base):
    __tablename__ = "SkillEmbedding"
    id = Column(Text, primary_key=True)
    skill = Column(String)
    normalizedSkill = Column(String)
    embedding = Column(Vector(384))
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)