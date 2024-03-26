from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from address_book.database.db import get_db
from address_book.schemas import ContactBase, ContactResponse
from address_book.database.models import Contact
from address_book.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts')


@router.get("/get_all", response_model=List[ContactResponse])
async def read_contacts(db: Session = Depends(get_db)):
    tags = await repository_contacts.get_contacts(db)
    return tags


@router.get("/get/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    tag = await repository_contacts.get_contact(contact_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return tag


@router.post("/create")
async def create_new(body: ContactBase, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/update/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/delete/{contact_id}")
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return 'Contact successfully deleted'


@router.get("/search")
async def search_contacts(query: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contacts(query, db)
    if len(contacts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nothing found")
    return contacts


@router.get("/search_birthdays")
async def search_birthdays(db: Session = Depends(get_db)):
    return await repository_contacts.get_birthdays(db)