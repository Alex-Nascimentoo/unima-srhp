from flask import Flask
from flask_cors import CORS
from src.modules.business.routes import bp as business_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(business_bp)

@app.route("/")
def health_check():
    return {
        'message': 'Service is up and running!',
        'status': 'OK'
    }, 200
