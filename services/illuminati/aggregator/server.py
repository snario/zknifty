from flask import Blueprint, request, jsonify
from dependency_config import container

api = Blueprint('api', __name__)
aggregator = Blueprint('aggregator', __name__)


@api.route('/proof/<uid>', methods=['GET'])
def get_proof(uid):
    return jsonify(
            {"uid": uid, 
            "proof": container.get_aggregator().get_proof(int(uid))})

@api.route('/owner/<uid>', methods=['GET'])
def get_owner(uid):
    return str(container.get_aggregator().get_owner(int(uid)))

@api.route('/coins', methods=['GET'])
def get_coins():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    # sig = int(request.args.get('sig'))
    return jsonify(container.get_aggregator().get_coins([x, y]))

@api.route('/send_tx', methods=['POST'])
def send_tx():
    uid = int(request.form['uid'])
    to_x = request.form['to_x']
    to_y = request.form['to_y']
    sig = request.form['sig']
    return container.get_aggregator().send_transaction(uid, [to_x, to_y], sig)

@aggregator.route('/submit_state', methods=['POST'])
def submit_state():
    return container.get_aggregator().submit_state()
