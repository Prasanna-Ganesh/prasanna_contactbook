from . import db
from datetime import datetime, date, timezone
from dataclasses import dataclass
@dataclass
class Contact(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.Text,unique=True, nullable=False)
    phone: int = db.Column(db.BigInteger,unique=True, nullable=False)
    email: str = db.Column(db.Text)
    
    create_time: date = db.Column(
        db.DateTime(timezone.utc), nullable=False, default=datetime.utcnow
    )
    modify_time: datetime = db.Column(
        db.DateTime(timezone.utc), nullable=False, default=datetime.utcnow
    )
