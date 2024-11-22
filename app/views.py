from app import app, db, admin
from flask_admin.contrib.sqla import ModelView
from .models import Property, Landlord

admin.add_view(ModelView(Property, db.session))
admin.add_view(ModelView(Landlord, db.session))


@app.route('/', methods=['GET', 'POST'])
def home():
    return "hello world"
