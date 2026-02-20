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