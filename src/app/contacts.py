from flask import request, jsonify,Blueprint
from . import db,app,CustomJSONEncoder
from .models import Contact
from .utils import add_contacts,edit_contact
from datetime import datetime as dt, timezone
import json

contact_book = Blueprint('contact_book', __name__, url_prefix='/api/contacts')


class ContactBookException(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code


@contact_book.errorhandler(ContactBookException)
def handle_scheduler_exception(e):
    app.logger.exception(e)
    return {"success": False, "error": e.message}, e.code

@contact_book.route('/', methods=['GET'])
def get_contacts():
    now = dt.now(timezone.utc)
    contact = Contact.query
    limit = int(request.args.get("limit", app.config["PAGE_LIMIT"]))
    sort = request.args.get("sort", "name")
    order = request.args.get("order", "asc")
    page_num = request.args.get("page", 1, type=int)
    search = request.args.get("search")

    if search:
        search_query = f"%{search}%"
        contact = contact.filter(Contact.name.ilike(search_query))

    sort = getattr(Contact, sort)
    order = contact.order_by(sort)

    paginated = order.paginate(page=page_num, per_page=limit, error_out=False)

    allContacts = paginated.items

    return {
        "success": True,
        "Contacts": allContacts,
        "timestamp": now,
        "currentPage": paginated.page,
        "totalPages": paginated.pages,
        "totalCount": contact.count(),
    }

@contact_book.route('/createcontacts', methods=['POST'])
def create_contact():
    data = request.json
    contacts = add_contacts(data)
    db.session.execute(contacts)
    db.session.commit()
    
    return jsonify({'message': 'Contacts created successfully'})


@contact_book.route('/upsertcontacts/', methods=['PUT'])
def upsert_contacts():
    data = request.json
    updated_contact=edit_contact(data)
    db.session.execute(updated_contact)
    db.session.commit()
    return jsonify({"message":"Contact updated"})

@contact_book.route('/<string:name>', methods=['DELETE'])
def delete_contact(name):
    contact = Contact.query.filter_by(name = name.upper()).first()

    if not contact:
        raise ContactBookException(f"Contact {name} not Found")
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact deleted successfully'})

@contact_book.route('/delete', methods=['DELETE'])
def delete_contacts():
    deleteContacts = request.json
    names_to_delete = [name.upper() for name in deleteContacts]
    contacts = Contact.query.filter(
        Contact.name.in_(names_to_delete)
    ).delete()

    if not contacts:
        raise ContactBookException(f"Contact not found {deleteContacts}")
    db.session.commit()
    return jsonify({'message': 'Contact deleted successfully'})



@contact_book.route('/export', methods=['GET'])
def export_data():
    contacts = Contact.query.all()
    contact_data=[]
    for contact in contacts:
        contact_dict={
            'id': contact.id,
            'name': contact.name,
            'phone': contact.phone,
            'email': contact.email,
            'create_time': contact.create_time,
            'modify_time': contact.modify_time

        }
        contact_data.append(contact_dict)
    json_data = json.dumps(contact_data, cls=CustomJSONEncoder)
    with open('contacts.json', 'w') as file:
        file.write(json_data)

    return jsonify({'message': 'Data exported to JSON file'})

