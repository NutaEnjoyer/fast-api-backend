"""
Base DTO (Data Transfer Object) module.

This module provides the base DTO class and utility functions
for handling data transfer between API layers with automatic
field name conversion and validation.
"""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


def alias_generator(field_name: str) -> str:
    """
    Generate camelCase alias from snake_case field name.

    Converts snake_case field names to camelCase for API responses.
    Handles special cases like leading underscores.

    Args:
        field_name: The snake_case field name to convert

    Returns:
        The camelCase version of the field name

    Examples:
        >>> alias_generator("user_id")
        "userId"
        >>> alias_generator("created_at")
        "createdAt"
        >>> alias_generator("_private_field")
        "_privateField"
    """
    parts = field_name.split("_")
    if parts[0] == "":
        parts[1] = "_" + parts[1]
        parts.pop(0)
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class BaseModelDto(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generator,
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True,
        json_encoders={datetime: lambda v: v.isoformat()},
    )


class BaseDto(BaseModel):
    """
    Base DTO class with common fields and configuration.

    Provides common fields like id, created_at, and updated_at
    that are shared across all DTOs in the application.
    Includes automatic camelCase conversion and ORM compatibility.
    """

    id: str = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(
        alias_generator=alias_generator,
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True,
        json_encoders={datetime: lambda v: v.isoformat()},
    )
