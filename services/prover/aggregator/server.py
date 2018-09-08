from flask import Blueprint, request
from prover.dependency_config import container

api = Blueprint('api', __name__)
aggregator = Blueprint('aggregator', __name__)

@api.route('/proof/<uid>', methods=['GET'])
def get_proof(uid):
    return container.get_aggregator().get_proof(int(uid))

@api.route('/owner/<uid>', methods=['GET'])
def get_owner(uid):
    return container.get_aggregator().get_owner(int(uid))

@api.route('/send_tx', methods=['POST'])
def send_tx():
    uid = int(request.form['uid'])
    to = request.form['to']
    sig = request.form['sig']
    return container.get_aggregator().send_transaction(uid, to, sig)

@aggregator.route('/submit_state', methods=['POST'])
def submit_state():
    return container.get_aggregator().submit_state()
