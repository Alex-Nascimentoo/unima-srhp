from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def health_check():
    return {
        'message': 'Service is up and running!',
        'status': 'OK'
    }, 200
