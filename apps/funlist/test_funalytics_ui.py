"""
Simple Flask tests to verify Funalytics UI integration.
"""
import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the current directory to Python path to import the Flask app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, db
    from models import Event, User
    import routes
except ImportError as e:
    print(f"Warning: Could not import Flask app: {e}")
    print("This test requires the Flask application to be properly configured.")
    app = None


class TestFunalyticsUI(unittest.TestCase):
    """Test Funalytics UI integration."""
    
    def setUp(self):
        """Set up test environment."""
        if app is None:
            self.skipTest("Flask app not available")
            
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        # Initialize routes
        routes.init_routes(self.app)
    
    @patch('routes.get_funalytics_scores')
    def test_events_page_renders_funalytics_scores(self, mock_get_scores):
        """Test that events page renders Funalytics scores correctly."""
        # Mock Funalytics scores
        mock_get_scores.return_value = {
            1: {
                'overallScore': 8,
                'communityVibe': 7,
                'familyFun': 9,
                'reasoning': 'Great family event with strong community engagement.'
            }
        }
        
        with self.app.app_context():
            with self.app.test_request_context():
                response = self.client.get('/events')
                
                # Check response is successful
                self.assertEqual(response.status_code, 200)
                
                # Check that Funalytics-related content is in the response
                response_data = response.get_data(as_text=True)
                
                # Look for Funalytics indicators (brain icon, score display)
                self.assertIn('fas fa-brain', response_data)
                self.assertIn('Community', response_data)
                self.assertIn('Family', response_data)
    
    @patch('routes.get_funalytics_scores')
    def test_event_detail_renders_funalytics_analysis(self, mock_get_scores):
        """Test that event detail page renders Funalytics analysis."""
        # Mock Funalytics scores for specific event
        mock_get_scores.return_value = {
            1: {
                'overallScore': 6,
                'communityVibe': 5,
                'familyFun': 7,
                'reasoning': 'Moderate fun event with good family appeal.',
                'computedAt': '2025-09-15T18:00:00Z'
            }
        }
        
        with self.app.app_context():
            with self.app.test_request_context():
                response = self.client.get('/events/1')
                
                # Check response is successful
                self.assertEqual(response.status_code, 200)
                
                response_data = response.get_data(as_text=True)
                
                # Look for Funalytics analysis section
                self.assertIn('Funalytics Analysis', response_data)
                self.assertIn('Moderate fun event', response_data)
                self.assertIn('Last computed:', response_data)
    
    @patch('routes.recompute_funalytics_score')
    def test_admin_recompute_button_functionality(self, mock_recompute):
        """Test admin recompute button works correctly."""
        mock_recompute.return_value = True
        
        with self.app.app_context():
            # Note: This test would require setting up authentication and admin user
            # For now, just test that the route exists
            with self.app.test_request_context():
                # Test that the route is registered
                url_map = self.app.url_map
                route_found = any(
                    '/admin/recompute-funalytics' in rule.rule 
                    for rule in url_map.iter_rules()
                )
                self.assertTrue(route_found, "Admin recompute route should be registered")
    
    def test_graceful_fallback_without_funalytics(self):
        """Test that pages work gracefully when Funalytics is unavailable."""
        with patch('routes.get_funalytics_scores') as mock_get_scores:
            # Mock API failure
            mock_get_scores.return_value = {}
            
            with self.app.app_context():
                with self.app.test_request_context():
                    response = self.client.get('/events')
                    
                    # Should still render successfully
                    self.assertEqual(response.status_code, 200)
                    
                    response_data = response.get_data(as_text=True)
                    
                    # Should fall back to star ratings
                    self.assertIn('⭐', response_data)


if __name__ == '__main__':
    unittest.main()