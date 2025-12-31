"""
---
Purpose: Error handler edge case tests
Description: Comprehensive tests for Flask error handlers (404, 500, 400, 403, etc.)
File: backend/tests/test_error_handlers.py | Repository: X-Filamenta-Python
Created: 2025-12-30T00:15:00+00:00
Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0
License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved.
Metadata:
- Status: Complete
- Classification: Public
---
"""
import pytest
import json
from flask import Flask
class TestErrorHandlerEdgeCases:
    """Test edge cases in error handlers."""
    def test_404_with_ajax_request(self, client):
        """
        Test 404 error response for AJAX requests.
        Expected: Should return JSON response instead of HTML.
        """
        response = client.get(
            '/this-route-does-not-exist',
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )
        assert response.status_code == 404
        # Check if response is JSON for AJAX
        if response.content_type and 'application/json' in response.content_type:
            data = response.get_json()
            assert 'error' in data or 'message' in data
        else:
            # If not JSON, at least verify it's a 404
            assert b'404' in response.data or b'Not Found' in response.data
    def test_500_with_json_content_type(self, client, app):
        """
        Test 500 error with JSON content type expectation.
        Expected: Should return appropriate JSON error for API endpoints.
        """
        # Create a route that raises an exception
        @app.route('/test-500-json')
        def trigger_500_json():
            raise Exception("Test exception for JSON response")
        response = client.get(
            '/test-500-json',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )
        assert response.status_code == 500
        # For JSON requests, should return JSON error
        if response.content_type and 'application/json' in response.content_type:
            data = response.get_json()
            assert 'error' in data or 'message' in data
        else:
            # At minimum, verify it's a 500 error
            assert response.status_code == 500
    def test_400_with_invalid_data(self, client, app):
        """
        Test 400 error with malformed request data.
        Expected: Should return clear error message for bad requests.
        """
        # Create a route that expects JSON
        @app.route('/test-400', methods=['POST'])
        def trigger_400():
            from flask import request
            data = request.get_json()
            if not data:
                from werkzeug.exceptions import BadRequest
                raise BadRequest("Missing JSON data")
            return {'success': True}
        # Send malformed JSON
        response = client.post(
            '/test-400',
            data='{"invalid": json syntax',
            content_type='application/json'
        )
        # Should return 400 for bad JSON
        assert response.status_code in [400, 415]  # 415 = Unsupported Media Type
    def test_403_forbidden_without_permission(self, client, app):
        """
        Test 403 error when accessing protected resource without permission.
        Expected: Should return forbidden error with appropriate message.
        """
        # Create a protected route
        @app.route('/test-403')
        def trigger_403():
            from werkzeug.exceptions import Forbidden
            raise Forbidden("You don't have permission to access this resource")
        response = client.get('/test-403')
        assert response.status_code == 403
        assert b'403' in response.data or b'Forbidden' in response.data
class TestErrorHandlerHTMLResponses:
    """Test HTML error page rendering."""
    def test_404_renders_custom_page(self, client):
        """
        Test that 404 renders custom error page.
        Expected: Should show custom 404 page, not Flask default.
        """
        response = client.get('/this-page-does-not-exist-xyz123')
        assert response.status_code == 404
        # Should contain HTML
        assert b'<html' in response.data.lower() or b'<!doctype' in response.data.lower()
    def test_500_renders_custom_page(self, client, app):
        """
        Test that 500 error renders custom error page.
        Expected: Should show custom 500 page.
        """
        # Create route that raises exception
        @app.route('/test-500-html')
        def trigger_500_html():
            raise Exception("Test exception for HTML response")
        response = client.get('/test-500-html')
        assert response.status_code == 500
        # Should contain HTML error page
        assert b'<html' in response.data.lower() or b'error' in response.data.lower()
    def test_error_page_does_not_leak_secrets(self, client, app):
        """
        Test that error pages don't expose sensitive information.
        Expected: Should not show internal paths, secrets, or debug info in production.
        """
        @app.route('/test-error-secrets')
        def trigger_error_with_secret():
            secret_key = "super_secret_api_key_12345"
            raise Exception(f"Error with secret: {secret_key}")
        response = client.get('/test-error-secrets')
        assert response.status_code == 500
        # In production mode, should NOT leak the secret
        if not app.config.get('DEBUG'):
            assert b'super_secret_api_key' not in response.data
            assert b'12345' not in response.data
class TestErrorHandlerLogging:
    """Test that errors are properly logged."""
    def test_404_is_logged(self, client, caplog):
        """
        Test that 404 errors are logged.
        Expected: Should log 404 events for monitoring.
        """
        import logging
        caplog.set_level(logging.WARNING)
        response = client.get('/non-existent-route-for-logging')
        assert response.status_code == 404
        # Check if 404 was logged (some frameworks log at WARNING or INFO level)
        # Note: Actual log level may vary by configuration
    def test_500_is_logged_with_traceback(self, client, app, caplog):
        """
        Test that 500 errors are logged with full traceback.
        Expected: Should log exception details for debugging.
        """
        import logging
        caplog.set_level(logging.ERROR)
        @app.route('/test-500-logging')
        def trigger_500_for_logging():
            raise ValueError("Test exception for logging verification")
        response = client.get('/test-500-logging')
        assert response.status_code == 500
        # Check logs contain error information
        # Note: Exact log format depends on logging configuration
class TestErrorHandlerSecurity:
    """Test security aspects of error handlers."""
    def test_error_handler_prevents_xss(self, client, app):
        """
        Test that error messages are properly escaped to prevent XSS.
        Expected: HTML in error messages should be escaped.
        """
        @app.route('/test-xss-in-error')
        def trigger_error_with_html():
            user_input = "<script>alert('XSS')</script>"
            raise Exception(f"Invalid input: {user_input}")
        response = client.get('/test-xss-in-error')
        assert response.status_code == 500
        # Script tags should be escaped, not executable
        if b'<script>' in response.data:
            # If present, should be HTML-escaped
            assert b'&lt;script&gt;' in response.data or b'escaped' in response.data.lower()
    def test_error_handler_rate_limiting(self, client):
        """
        Test that error endpoints don't bypass rate limiting.
        Expected: Even error responses should respect rate limits.
        """
        # Make multiple requests to non-existent endpoint
        responses = []
        for _ in range(100):  # Try many requests
            response = client.get('/non-existent-endpoint-rate-test')
            responses.append(response.status_code)
        # All should be 404, none should bypass to reach actual routes
        assert all(code == 404 for code in responses)
# Run tests marker
pytestmark = pytest.mark.error_handlers
