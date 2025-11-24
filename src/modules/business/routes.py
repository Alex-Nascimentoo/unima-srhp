from flask import Blueprint
from src.modules.category.routes import category_bp

bp = Blueprint('business', __name__, url_prefix='/business')

bp.register_blueprint(category_bp)  
# Example route
@bp.route('/info', methods=['GET'])
def get_business_info():
    return {"business": "info"}
