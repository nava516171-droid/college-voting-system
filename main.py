from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import auth, elections, candidates, votes, otp, face, admin, candidate

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="College Voting System API",
    description="Backend API for college voting system with face recognition",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(elections.router)
app.include_router(candidates.router)
app.include_router(candidate.router)
app.include_router(votes.router)
app.include_router(otp.router)
app.include_router(face.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to College Voting System API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
