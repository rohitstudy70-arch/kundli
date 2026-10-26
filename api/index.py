import sys
import os
import urllib.parse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app

# WSGI Middleware to restore original PATH_INFO using __path parameter from vercel.json
class VercelPathFixer:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        qs = environ.get('QUERY_STRING', '')
        if '__path=' in qs:
            params = urllib.parse.parse_qs(qs, keep_blank_values=True)
            if '__path' in params:
                original_path = params['__path'][0]
                if not original_path.startswith('/'):
                    original_path = '/' + original_path
                environ['PATH_INFO'] = original_path

                # Remove __path from query string so Flask app doesn't see it
                del params['__path']
                environ['QUERY_STRING'] = urllib.parse.urlencode(params, doseq=True)
        elif environ.get('PATH_INFO', '') in ('/api/index', '/api/index/'):
            environ['PATH_INFO'] = '/'

        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathFixer(app.wsgi_app)
