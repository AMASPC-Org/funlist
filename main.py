
from app import app

if __name__ == "__main__":
    try:
        app.run(
            host='0.0.0.0',
            port=8080,
            debug=True
        )
    except Exception as e:
        print(f"Error starting server: {e}")
