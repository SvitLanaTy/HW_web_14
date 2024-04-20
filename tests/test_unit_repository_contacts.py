import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    delete_contact,
    search_contacts,
    days_to_birthday,
    get_upcoming_birthdays
)
from src.schemas.contact import ContactSchema


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self) -> None:
        self.user = User(id=1, username='test_user', email="test_user@gmail.com", password="password", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)
        
        

    async def test_get_contact(self):
        contact = Contact(id=1, first_name="test1", last_name="test2", email="test@gmail.com", phone_number="+380123456789", birthday=datetime.now().date(), extra_data="test_extra")
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contact
        result = await get_contact(1, self.session, self.user)
        self.assertEqual(result, contact)


    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [
            Contact(id=1, first_name="test1n", last_name="test1l", email="test1@gmail.com", phone_number="+380123456789", birthday=datetime.now().date(), extra_data="test_extra1"),
            Contact(id=2, first_name="test2n", last_name="test2l", email="test2@gmail.com", phone_number="+380123456789", birthday=datetime.now().date(), extra_data="test_extra2")]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)
        

    async def test_create_contact(self):
        body = ContactSchema(first_name="test1n", last_name="test1l", email="test1@gmail.com", phone_number="+380123456789", birthday=datetime.now().date(), extra_data="test_extra1")
        result = await create_contact(body, self.session, self.user)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.extra_data, body.extra_data)
      

    async def test_update_contact(self):
        body = ContactSchema(first_name="test", last_name="test2", email="test2@gmail.com", phone_number="+380123456789", birthday=datetime.now().date(), extra_data="test_extra2")
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, first_name="test", last_name="test2", email="test2@gmail.com", phone_number="+380123456789", birthday=datetime.now().date(), extra_data="test_extra2")
        self.session.execute.return_value = mocked_contact
        result = await update_contact(body, 1, self.session, self.user)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.extra_data, body.extra_data)
        

    async def test_delete_contact(self):        
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, first_name="test1", last_name="test2", email="test@gmail.com", phone_number="+380123456789", birthday=datetime.now().date(), extra_data="test_extra")
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertIsInstance(result, Contact)

    async def test_search_contacts(self):
        first_name = "test1n"
        last_name = "test1l"
        email = "test1@gmail.com"
        contacts = [
            Contact(id=1, first_name="test1n", last_name="test1l", email="test1@gmail.com", phone_number="+380123456789", birthday=datetime.now().date(), extra_data="test_extra1"),
            Contact(id=2, first_name="test2n", last_name="test1l", email="test2@gmail.com", phone_number="+380123456789", birthday=datetime.now().date(), extra_data="test_extra2")]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await search_contacts(first_name, last_name, email, self.session, self.user)
        self.assertEqual(result, contacts)


    async def test_get_upcoming_birthdays(self):
        limit = 10
        offset = 0
        contacts = [
            Contact(id=1, first_name="test1n", last_name="test1l", email="test1@gmail.com", phone_number="+380123456789", birthday=datetime.now().date() + timedelta(days=2), extra_data="test_extra1"),
            Contact(id=1, first_name="test2n", last_name="test2l", email="test2@gmail.com", phone_number="+380123456789",  birthday=datetime.now().date() + timedelta(days=3), extra_data="test_extra2")
        ]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_upcoming_birthdays(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)
