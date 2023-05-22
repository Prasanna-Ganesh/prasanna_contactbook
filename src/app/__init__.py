from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        from datetime import datetime, date
        if isinstance(obj, (date,datetime)):
            return obj.isoformat()
        return super().default(obj)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'prasanna'   
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://hello_flask:hello_flask@localhost/contact_book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "static/uploads"
app.config['PAGE_LIMIT'] = 10
app.config['MAX_PAGE_LIMIT'] = 10000000000
db = SQLAlchemy(app)


try:
    from . import (models, contacts)
    with app.app_context():
        models.db.create_all()

    app.register_blueprint(contacts.contact_book)
    
  
except Exception as e:
    import traceback

    traceback.print_exc()
    app.logger.error(e)
