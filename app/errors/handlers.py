from werkzeug.exceptions import NotFound, InternalServerError
from flask import render_template
from app.errors import errors_bp
from app import db


@errors_bp.app_errorhandler(NotFound)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@errors_bp.app_errorhandler(InternalServerError)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
