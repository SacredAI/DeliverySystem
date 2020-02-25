import flask as f
import deliverysystem as d
from .tracking import orders

d_bp = f.Blueprint('delivery', __name__)


@d_bp.route('/tracking', methods=['POST'])
def tracking():
    return orders()
