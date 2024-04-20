import unittest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import MagicMock, AsyncMock
from src.entity.models import User
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    change_password
)
from src.schemas.user import UserSchema

class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self) -> None:
        self.user = User(username="test_user", password="test_psw", email="test@example.com", confirmed=True, avatar="test_avatar")
        self.db_session = AsyncMock(spec=AsyncSession)

    async def test_get_user_by_email(self):
        user = User(email="test@example.com", username="test_user", password="test_psw")
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.db_session.execute.return_value = mocked_user
        result = await get_user_by_email("test@example.com", self.db_session)
        self.assertEqual(result, user)

    async def test_create_user(self):        
        body = UserSchema(username="test_user", password="test_psw", email="test@example.com")
        result = await create_user(body, self.db_session)
        self.assertIsInstance(result, User)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.username, body.username)
        

    async def test_update_token(self):
        user = User(email="test@example.com", username="test_user", password="test_psw")
        await update_token(user, "new_token", self.db_session)
        self.assertEqual(user.refresh_token, "new_token")
        self.db_session.commit.assert_awaited_once()

    async def test_confirmed_email(self):
        email = "test@example.com"
        mocked_user = MagicMock()
        mocked_user.get_user_by_email(email, self.db_session).return_value = self.user
        self.db_session.execute.return_value = mocked_user
        await confirmed_email(email=email, db=self.db_session)
        self.assertEqual(self.user.confirmed, True)
        self.db_session.commit.assert_awaited_once()

    
    async def test_change_password(self):
        user = User(email="test@example.com", username="test_user", password="test_password")
        await change_password(user, "new_password", self.db_session)
        self.assertEqual(user.password, "new_password")
        self.db_session.commit.assert_awaited_once()
        
