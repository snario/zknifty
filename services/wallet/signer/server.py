from flask import Blueprint, request
from dependency_config import container

api = Blueprint('api', __name__)
signer = Blueprint('signer', __name__)

@api.route('/sign_transfer', methods=['POST'])
def transfer():
    content = request.get_json()
    receiver_pub_key = content['receiver_pub_key']
    token_id = content['token_id']

    return container.get_signer().sign_transfer(receiver_pub_key, token_id)

@api.route('/verify_proof', methods=['GET'])
def verify_proof():
    root = request.form['root']
    token_id = int(request.form['token_id'])
    proof = request.form['proof']

    return container.get_signer().verify_proof(root, token_id, proof)

@api.route('/pub_key', methods=['GET'])
def pub_key():
    return container.get_signer().pub_key()