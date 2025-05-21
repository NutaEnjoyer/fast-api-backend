from pydantic import BaseModel, ConfigDict
from datetime import datetime

def alias_generator(field_name: str) -> str:
    parts = field_name.split('_')
    if parts[0] == '': parts[1] = '_' + parts[1]; parts.pop(0)
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


class BaseDto(BaseModel):
    id: str
    createdAt: datetime
    updatedAt: datetime

    model_config = ConfigDict(
        alias_generator=alias_generator,
        populate_by_name=True,
        from_attributes=True,
        orm_mode=True,
        use_enum_values=True
    )
