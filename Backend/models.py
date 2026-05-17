from sqlalchemy import Integer, String, Boolean  # type: ignore[import]
from sqlalchemy.orm import Mapped, mapped_column  # type: ignore[import]
from .database import Base  # type: ignore[assignment]

class User(Base):  # type: ignore[valid-type]
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    # Simple privacy + role flags for v1
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    share_activity_with_earth: Mapped[bool] = mapped_column(Boolean, default=True)
    show_real_name_in_classrooms: Mapped[bool] = mapped_column(Boolean, default=False)
