from flask import Blueprint, request
from dependency_config import container

api = Blueprint('api', __name__)
signer = Blueprint('signer', __name__)

@api.route('/transfer', methods=['POST'])
def transfer():
    content = request.get_json()
    receiver_pub_key = content['receiver_pub_key']
    token_id = content['token_id']

    return container.get_signer().transfer(receiver_pub_key, token_id)

@api.route('/get_proof', methods=['GET'])
def get_proof(token_id):
    return container.get_signer().get_proof(int(token))

@api.route('/get_tokens', methods=['GET'])
def get_tokens():
    return container.get_signer().get_tokens()