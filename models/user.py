from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import String, DateTime, func
from pydantic import EmailStr


class User(SQLModel, table=True):
    """User model with email validation and audit fields."""
    
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=50)
    email: EmailStr = Field(unique=True, sa_type=String(255))
    password: str = Field(max_length=255)
    name: str = Field(max_length=100)
    surname: str = Field(max_length=100)
    disabled: bool = Field(default=False)
    
    # Campos de auditoría - TIMESTAMP para trazabilidad del sistema
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_type=DateTime(timezone=True)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}
    )

    