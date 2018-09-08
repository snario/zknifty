# Flask API for submitting info / retrieving data

`python -m aggregator` to launch

## Example interaction

### Send token
`curl http://localhost:8546/send_tx -d "uid=0&to=0x1234&sig=0x1234`

### Get the owenr of a token
`curl http://localhost:8546/owner/0`


