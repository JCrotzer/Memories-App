from flask_app import create_app, db

app = create_app()

with app.app_context():
    # db.drop_all()
    db.create_all()
    # print("✅ All tables created successfully!")