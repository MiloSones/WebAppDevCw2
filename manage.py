from app import app,db
from app.models import populate_products



with app.app_context():
    db.create_all()  # Ensure all tables are created
    populate_products()
