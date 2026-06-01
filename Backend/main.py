from fastapi import FastAPI  # type: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[reportMissingImports]
from .database import Base, engine  # type: ignore
from .auth import router as auth_router  # type: ignore
from .classroom import router as classroom_router  # type: ignore

Base.metadata.create_all(bind=engine)  # type: ignore[reportUnknownMemberType]

app = FastAPI(title="Mars Habitat OS") # pyright: ignore[reportUnknownVariableType]

app.add_middleware(  # type: ignore[reportUnknownMemberType]
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)  # type: ignore[reportUnknownMemberType]
app.include_router(classroom_router)  # type: ignore[reportUnknownMemberType]

@app.get("/health")  # type: ignore[reportUnknownMemberType, reportUntypedFunctionDecorator]
def health() -> dict[str, str]:
    return {"status": "ok", "location": "Mars Habitat OS v1"}
