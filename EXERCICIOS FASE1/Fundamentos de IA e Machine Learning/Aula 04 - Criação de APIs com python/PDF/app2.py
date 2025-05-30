from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    return render_template('login.html')


app.register_blueprint(auth_bp, url_prefix='/auth')
