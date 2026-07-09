from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    file_name = Column(
        String(255),
        nullable=False
    )

    file_path = Column(
        String(500),
        nullable=False
    )

    candidate_name = Column(
        String(100),
        nullable=True
    )

    candidate_email = Column(
        String(150),
        nullable=True
    )

    candidate_phone = Column(
        String(50),
        nullable=True
    )

    skills = Column(
        Text,
        nullable=True
    )

    parsed_text = Column(
        Text,
        nullable=True
    )

    uploaded_at = Column(
        DateTime,
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="resumes"
    )

    interviews = relationship(
        "Interview",
        back_populates = "resume",
        cascade = "all, delete-orphan")