from flask import Blueprint

publication_bp = Blueprint('publication', __name__)

# Example route
@publication_bp.route('/', methods=['GET'])
def get_publication():
    return {"code": 200, "status": "success", "message": "Publication endpoint"}