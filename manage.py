from app import app,db
from app.models import set_fake_stock



with app.app_context():
    db.create_all()  # Ensure all tables are created
    set_fake_stock()
