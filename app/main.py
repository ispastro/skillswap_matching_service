from fastapi  import FastAPI
from app.config import settings
 

app = FastAPI(title = settings.app_name)
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