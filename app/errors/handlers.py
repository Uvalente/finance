from werkzeug.exceptions import NotFound
from flask import render_template
from app.errors import errors_bp

@errors_bp.app_errorhandler(NotFound)
def not_found_error(error):
    print('#############################')
    return render_template('errors/404.html'), 404
