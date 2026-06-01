from sqlalchemy import Integer, String, Boolean  # type: ignore[import]
from sqlalchemy.orm import Mapped, mapped_column  # type: ignore[import]
from .database import Base  # type: ignore[assignment]

class User(Base):  # type: ignore[valid-type]
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)  # type: ignore[reportUnknownVariableType]
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)  # type: ignore[reportUnknownVariableType]
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)  # type: ignore[reportUnknownVariableType]

    # Simple privacy + role flags for v1
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)  # type: ignore[reportUnknownVariableType]
    share_activity_with_earth: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)  # type: ignore[reportUnknownVariableType]
    show_real_name_in_classrooms: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)  # type: ignore[reportUnknownVariableType]
