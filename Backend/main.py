from fastapi import FastAPI  # type: ignore[import]
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import]
from .database import Base, engine  # type: ignore
from .auth import router as auth_router  # type: ignore
from .classroom import router as classroom_router  # type: ignore

Base.metadata.create_all(bind=engine)  # type: ignore[reportUnknownMemberType]

app: FastAPI = FastAPI(title="Mars Habitat OS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(classroom_router)

@app.get("/health")
def health():
    return {"status": "ok", "location": "Mars Habitat OS v1"}
