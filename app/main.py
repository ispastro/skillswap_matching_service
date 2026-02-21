from fastapi  import FastAPI
from app.config import settings
 
from app.api.routes import router


app = FastAPI(title = settings.app_name)
app.include_router(router)

@app.get("/")
def root():
    return { "Message": f"Welcome to the {settings.app_name}!"}

@app.get("/health")    
def health():
    return {
        "status": "healthy",
        "service name": settings.app_name,
        "port": settings.port
        }


@app.get("/db-test")
def test_database():
    from sqlalchemy import text
    from app.models.database import engine
    try:
        with engine.connect() as connection:
            result =connection.execute(text("SELECT 1"))
            return {"status": "Database connection successful", "message": "Connection to database was successful."}
    except Exception as e:
        return {"status": "Database connection failed", "message": str(e)}

@app.get("/embedding-test")
def  test_embedding():
    from app.services.embedding_service import embedding_service

    text ="React developer"
    embedding =embedding_service.generate_embeddings(text)
    return {
        "text": text,
        "embedding_length": len(embedding),
        "first_five_values": embedding[:5],
        "message": "Embedding generated successfully"
    }


@app.get("/similarity-test")
def test_similarity():
    from app.services.embedding_service import embedding_service
    import numpy as np
    react =embedding_service.generate_embeddings("React developer")
    vue = embedding_service.generate_embeddings("Vue developer")
    chef = embedding_service.generate_embeddings("Chef")

    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    similarity_react_vue = cosine_similarity(react, vue)
    similarity_react_chef = cosine_similarity(react, chef)
    return {
        "react_vue_similarity": round(float(similarity_react_vue), 2),
        "react_chef_similarity": round(float(similarity_react_chef), 2),
        "message":"Similarity calculated successfully"
    }
@app.get("/setup-pgvector")
def setup_pgvector():
        from sqlalchemy import text
        from app.models.database import engine
        try:
            with engine.connect()  as connection:
                connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                connection.commit()
                return {"status": "pgvector setup successful", "message": "pgvector extension is set up successfully."}
        except  Exception as e:
            return  {"status":"error", "message": str(e)} 


@app.get("/check_tables")
def check_tables():
    from sqlalchemy import text, inspect
    from app.models.database import engine
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if "SkillEmbedding" in tables:
            columns = inspector.get_columns("SkillEmbedding")
            column_info = [{"name": col["name"], "type": str(col["type"])} for col in columns]
            return {
                "table_exists": True,
                "columns": column_info
            }
        else:
            return {
                "table_exists": False,
                "tables": tables,
                "message": "SkillEmbedding table not found"
            }
    except Exception as e:
        return {
            "table_exists": False,
            "status": "error",
            "message": str(e)
        }


@app.get("/fix-embedding-column")
def fix_embedding_column():
    from sqlalchemy import text
    from app.models.database import engine
    try:
        with engine.connect()  as connection:
            connection.execute(text('ALTER TABLE "SkillEmbedding" DROP COLUMN IF EXISTS embedding'))  
            connection.execute(text('ALTER TABLE "SkillEmbedding" ADD COLUMN embedding vector(384)'))
            connection.commit()
            return {"status": "success", "message": "Embedding column fixed!  it's now vector(384)"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/check-real-column-type")
def check_real_column_type():
    from sqlalchemy import text
    from app.models.database import engine
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT column_name, data_type, udt_name
                FROM information_schema.columns
                WHERE table_name = 'SkillEmbedding'
                AND column_name = 'embedding'
            """))
            
            row = result.fetchone()
            if row:
                return {
                    "column_name": row[0],
                    "data_type": row[1],
                    "udt_name": row[2],
                    "message": "If udt_name is 'vector', it's correct!"
                }
            else:
                return {"status": "error", "message": "Column not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
@app.get("/test-read-users")
def test_read_users():
    from app.models.database import SessionLocal
    from app.models.schemas import User
    
    db = SessionLocal()
    try:
        # Get first 3 users
        users = db.query(User).limit(3).all()
        
        result = []
        for user in users:
            result.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "skillsHave": user.skillsHave,
                "skillsWant": user.skillsWant
            })
        
        return {
            "count": len(result),
            "users": result
        }
    finally:
        db.close()


@app.get("/check-user-columns")
def check_user_columns():
    from sqlalchemy import text, inspect
    from app.models.database import engine
    
    try:
        inspector = inspect(engine)
        columns = inspector.get_columns("User")
        column_names = [col["name"] for col in columns]
        
        return {
            "table": "User",
            "columns": column_names
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/test-alice-bob-match")
def test_alice_bob_match():
    from app.services.matching_service import matching_service
    
    # Alice's skills
    alice_wants = ["Python", "Django", "Machine Learning"]
    alice_has = ["JavaScript", "React", "TypeScript", "CSS"]
    
    # Bob's skills
    bob_has = ["Python", "Django", "PostgreSQL", "Docker"]
    bob_wants = ["JavaScript", "React", "AWS"]
    
    # Calculate match from Alice's perspective
    result = matching_service.calculate_match_score(
        my_skills_want=alice_wants,
        my_skills_have=alice_has,
        their_skills_have=bob_has,
        their_skills_want=bob_wants
    )
    
    return {
        "alice_wants": alice_wants,
        "alice_has": alice_has,
        "bob_has": bob_has,
        "bob_wants": bob_wants,
        "match_result": result
    }
