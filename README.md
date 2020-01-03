Flask-HTTPAuth with digital signature
==============
Simple extension that provides HTTP authentication with digital signature for Flask routes.

Installation
------------
The easiest way to install this is through pip.
```
pip install Flask-HTTPAuth
```

Source code of example
----------------------------
```python
from flask import Flask, jsonify, g
from flask_httpauth import HTTPTokenAuth
from app.utils.digital_signatures import sign, verify
from config import Config

PUBLIC_KEY = '77c300e5871fa9889ead09d6562b2b430112c39abe205bde'
SECRET_KEY = '980d92b01709aed6c6a0c181e1d99db336e723da4130b844'
TOKEN = sign(PUBLIC_KEY, SECRET_KEY)

tokens = {
    TOKEN:'iness@example.com'
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
        return jsonify({'auth':g.current_user})

    return app
```

Functions for create keys, digital signature and verify digital signature
----------------------------
```python
from hashlib import blake2b
from hmac import compare_digest
from os import urandom
from binascii import hexlify

def create_key(): # create random key
    return hexlify(urandom(24)).decode('utf-8') 
    
def sign(public_key, secret_key): # create digital signature from public_key and secret key
    public_key = public_key.encode('utf-8')
    secret_key = secret_key.encode('utf-8')
    h = blake2b(digest_size=24, key=secret_key)
    h.update(public_key)
    return h.hexdigest()

def verify(public_key, secret_key, sig): # verify digital signature
    good_sig = sign(public_key, secret_key)
    return compare_digest(good_sig, sig)
```

Resources
---------

- [Documentation of flask-httpauth](http://flask-httpauth.readthedocs.io/en/latest/)
- [Documentation of python hashlib](https://docs.python.org/3/library/hashlib.html)
- [Examples from Miguel Grinberg](https://github.com/miguelgrinberg/Flask-HTTPAuth)
- [PyPI](https://pypi.org/project/Flask-HTTPAuth)
