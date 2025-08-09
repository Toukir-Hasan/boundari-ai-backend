# app/models/survey.py
# Purpose: define the Survey table

from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime, func, Index
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

class Survey(Base):
    __tablename__ = "surveys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prompt_raw: Mapped[str] = mapped_column(Text, nullable=False)                # original user input
    prompt_normalized: Mapped[str] = mapped_column(String(220), nullable=False)  # lower/trimmed form
    survey_json: Mapped[dict] = mapped_column(JSONB, nullable=False)             # generated survey
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Unique index for caching logic
    __table_args__ = (
        Index("uq_prompt_normalized", "prompt_normalized", unique=True),
    )
