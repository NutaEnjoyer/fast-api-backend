"""
Base service module providing common service operations.

This module contains the BaseService class which serves as a foundation
for all service classes in the application, providing common patterns
for data transformation and business logic operations.

The BaseService provides utility methods for converting between different
data formats and implementing common service layer patterns.
"""

from typing import Type, TypeVar, Any, Dict
from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class BaseService:
    """
    Base service class providing common service operations.

    This class serves as a foundation for all service classes,
    providing common patterns for data transformation and business
    logic operations. It implements utility methods that can be
    inherited by specific service classes.

    The BaseService provides methods for converting between different
    data formats (e.g., ORM models to DTOs) and implementing common
    service layer patterns.
    """

    def _to_dto(self, dto_class: Type[T], data: Any) -> T:
        """
        Convert data to a Pydantic DTO (Data Transfer Object).

        This method provides a standardized way to convert various data
        formats (dict, ORM models, etc.) to Pydantic DTOs for consistent
        data validation and serialization.

        Args:
            dto_class: The Pydantic model class to convert to
            data: The data to convert (can be dict, ORM model, etc.)

        Returns:
            Instance of the specified DTO class

        Raises:
            ValidationError: If data doesn't match DTO schema
        """
        return dto_class.model_validate(data)

    def _to_dict(self, data: Any) -> Dict[str, Any]:
        """
        Convert data to a dictionary format.

        This method provides a standardized way to convert various data
        formats to dictionaries for serialization or further processing.

        Args:
            data: The data to convert (can be Pydantic model, ORM model, etc.)

        Returns:
            Dictionary representation of the data
        """
        if hasattr(data, "model_dump"):
            return data.model_dump()
        elif hasattr(data, "__dict__"):
            return data.__dict__
        else:
            return dict(data)

    def _validate_data(self, data: Dict[str, Any], required_fields: list[str]) -> bool:
        """
        Validate that required fields are present in data.

        Args:
            data: Dictionary containing the data to validate
            required_fields: List of field names that must be present

        Returns:
            True if all required fields are present, False otherwise
        """
        return all(field in data for field in required_fields)
