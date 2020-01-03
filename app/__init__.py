from flask import Flask, jsonify, g
from flask_httpauth import HTTPTokenAuth
from app.utils.digital_signatures import sign, verify
from config import Config

"""
To gain access, you can use a command line HTTP client such as curl, passing
the encrypted token token:
    url -X GET -H "Authorization: Bearer <digital signature>" http://localhost:5000/
The response should include the username, which is obtained from the token.

For get digital signature for your token use PUBLIC_KEY and SECRET_KEY in sign function
digital signature = sign(PUBLIC_KEY, SECRET_KEY)

You can find sign function in /app/utils/digital_signatures.py
"""

PUBLIC_KEY = '77c300e5871fa9889ead09d6562b2b430112c39abe205bde'
SECRET_KEY = '980d92b01709aed6c6a0c181e1d99db336e723da4130b844'
TOKEN = sign(PUBLIC_KEY, SECRET_KEY)

tokens = {
    TOKEN: 'iness@example.com'
    }
auth = HTTPTokenAuth(scheme='Bearer')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @auth.verify_token
    def verify_token(digital_signature):
        if digital_signature in tokens:
            if verify(PUBLIC_KEY, SECRET_KEY, digital_signature):
                g.current_user = tokens[digital_signature]
                return True
            return False
        return False

    @app.route('/')
    def index():
        return '<a href="/api">Request to server without HTTP Authorization</a>'

    @app.route('/api')
    @auth.login_required
    def api():
        return jsonify({'auth': g.current_user})

    return app
