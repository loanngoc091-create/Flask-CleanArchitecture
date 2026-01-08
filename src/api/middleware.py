from flask import request, jsonify

def setup_middleware(app):
    @app.before_request
    def log_request_info():
        app.logger.debug('Headers: %s', request.headers)
        app.logger.debug('Body: %s', request.get_data())

    @app.after_request
    def add_custom_headers(response):
        response.headers['X-Custom-Header'] = 'Value'
        return response

    @app.errorhandler(Exception)
    def handle_exception(error):
        response = jsonify({'error': str(error)})
        response.status_code = 500
        return response
