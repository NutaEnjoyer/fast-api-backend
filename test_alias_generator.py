"""
Test script to verify alias_generator functionality.
"""

from app.dto.user_dto import UpdateUserDto


def test_alias_generator():
    """Test that camelCase field names are properly converted."""

    # Test data with camelCase field names
    test_data = {
        "email": "test@example.com",
        "workInterval": 25,  # camelCase
        "breakInterval": 5,  # camelCase
        "intervalCount": 4,  # camelCase
    }

    try:
        # Create UpdateUserDto from camelCase data
        dto = UpdateUserDto(**test_data)
        print("✅ Successfully created DTO from camelCase data")
        print(f"DTO fields: {dto.model_dump()}")

        # Test conversion back to camelCase
        camel_case_data = dto.model_dump(by_alias=True)
        print(f"✅ CamelCase output: {camel_case_data}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    test_alias_generator()
