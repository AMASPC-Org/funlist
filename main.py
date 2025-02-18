
from flask import Flask
from app import app

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=8080, debug=True)
