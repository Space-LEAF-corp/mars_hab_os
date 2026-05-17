try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session, sessionmaker, declarative_base
except ImportError as exc:
    raise ImportError(
        "SQLAlchemy is required to run this application. "
        "Install it with: pip install sqlalchemy"
    ) from exc

DATABASE_URL = "sqlite:///./mars_hab_os.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()
