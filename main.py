
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    # Ensure host is 0.0.0.0 to be accessible
    app.run(host='0.0.0.0', port=port, debug=False)
