from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, PastDate


class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = EmailStr()
    phone: str = Field(max_length=10)
    birthday: datetime = PastDate()


class ContactResponse(ContactBase):
    class Config:
        orm_mode = True