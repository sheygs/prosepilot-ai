from flask import Blueprint

content_bp = Blueprint('content', __name__)

# Example route
@content_bp.route('/', methods=['GET'])
def get_content():
    return {"code": 200, "message": "Content endpoint", "status": "success"}