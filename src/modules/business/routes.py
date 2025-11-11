from flask import Blueprint

bp = Blueprint('business', __name__, url_prefix='/business')

# Example route
@bp.route('/info', methods=['GET'])
def get_business_info():
    return {"business": "info"}
