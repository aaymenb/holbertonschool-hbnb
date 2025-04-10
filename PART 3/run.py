import os
from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
        print("Database tables created successfully!")
    app.run(host='0.0.0.0', port=5000, debug=True) 