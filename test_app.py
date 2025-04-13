
import logging
from app import create_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_app_initialization():
    """Test if the app can be initialized properly"""
    try:
        logger.info("Testing app initialization...")
        app = create_app()
        logger.info("App initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize app: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    success = test_app_initialization()
    if success:
        print("✅ App initialization test passed!")
    else:
        print("❌ App initialization test failed!")
