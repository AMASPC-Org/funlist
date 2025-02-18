
from app import app, db

if __name__ == "__main__":
    try:
        print("Starting Flask server...")
        with app.app_context():
            db.create_all()
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        print(f"Error starting server: {e}")
