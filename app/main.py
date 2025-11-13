from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.routes import auth, users

app = FastAPI(title="FastAPI Auth Service", version="1.0.0")

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/health")
def health():
    return {"status": "ok"}