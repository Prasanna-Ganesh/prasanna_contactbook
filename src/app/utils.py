from . import db
from .models import Contact
from sqlalchemy.dialects.postgresql import insert


# class ContactBookException(Exception):
#     def __init__(self, message, code=400):
#         self.message = message
#         self.code = code


def add_contacts(data):

    contacts =[]
    for contact in data:
        name = contact.get('name')
        phone = contact.get('phone')
        email = contact.get('email')
        
        contacts.append({'name':name.upper(),'phone':phone,'email':email})
      
    save = insert(Contact).values(contacts)
    save = save.on_conflict_do_nothing()
    
    return save

def edit_contact(data):
    contact_values = []
    for contact in data:
        name = contact.get('name')
        phone = contact.get('phone')
        email = contact.get('email')
        contact_values.append({'name': name.upper(), 'phone': phone, 'email': email})

    save = insert(Contact).values(contact_values)
    save = save.on_conflict_do_update(
        index_elements=['name'],
        set_={'phone': save.excluded.phone, 'email': save.excluded.email}
    )
    return save