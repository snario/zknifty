# Flask API

`python -m signer` to launch

## Example Interaction

### Transfer Token

`curl http://localhost:8547/transfer -H "Content-Type: application/json" -d '{"receiver_pub_key": [11607218079627653052025766014402194752294530688391339421323326354495267067619, 19303972550233461034811892118625032803630725251866462888625398884813627772712], "token_id": 2}'`

## Get Proof For Token

`curl http://localhost:8547/get_proof/0`

### Get All Owned Tokens

`curl http://localhost:8547/get_tokens`
