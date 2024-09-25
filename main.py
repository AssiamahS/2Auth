from flask import Flask, request, render_template, redirect, url_for
import pyotp
import qrcode
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)

# Secret key for the user (in a real app, store this securely)
user_secret = pyotp.random_base32()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/qrcode')
def qrcode_route():
    totp = pyotp.TOTP(user_secret)
    uri = totp.provisioning_uri("user@example.com", issuer_name="MyApp")
    img = qrcode.make(uri)
    buf = BytesIO()
    img.save(buf)
    img_b64 = b64encode(buf.getvalue()).decode('utf-8')
    return render_template('qrcode.html', img_data=img_b64)

@app.route('/verify', methods=['POST'])
def verify():
    token = request.form['token']
    totp = pyotp.TOTP(user_secret)
    if totp.verify(token):
        return "Verified!"
    else:
        return "Invalid token!", 400

if __name__ == '__main__':
    app.run(debug=True)
