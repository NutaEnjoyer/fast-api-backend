

from sqlalchemy import delete, select
from app.core.database import UserOrm
from app.dto.auth_dto import AuthDto
from app.dto.user_dto import UpdateUserDto
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    
    async def create(self, data: AuthDto) -> UserOrm:
        async with self.session() as session:
            user = UserOrm(**data.model_dump())
            session.add(user)
            await session.flush()
            await session.commit()
            await session.refresh(user)
            return user
        
    async def find_by_email(self, email: str) -> UserOrm | None:
        async with self.session() as session:
            query = select(UserOrm).where(UserOrm.email == email)
            result = await session.execute(query)
            user = result.scalars().first()
            return user
    
    async def find_by_id(self, id: str) -> UserOrm | None:
        async with self.session() as session:
            query = select(UserOrm).where(UserOrm.id == id)
            result = await session.execute(query)
            user = result.scalars().first()
            return user
        
    async def update(self, id: str, data: UpdateUserDto) -> UserOrm:
        async with self.session() as session:
            query = select(UserOrm).where(UserOrm.id == id)
            result = await session.execute(query)
            user = result.scalars().first()

            if not user:
                raise ValueError(f"User with id {id} not found")
            
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(user, key, value)

            await session.flush()
            await session.commit()
            await session.refresh(user)
            return user 
    
    async def delete(self, id: str) -> None:
        async with self.session() as session:
            query = delete(UserOrm).where(UserOrm.id == id)
            await session.execute(query)
            
            await session.commit()
            return id