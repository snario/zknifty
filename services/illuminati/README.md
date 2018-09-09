# Flask API for submitting info / retrieving data

`python -m aggregator` to launch

## Example interaction

### Send token
`curl http://localhost:8546/send_tx -d "uid=0&to=0x1234&sig=0x1234`

### Get the owenr of a token
`curl http://localhost:8546/owner/0`

### Retrieve ownership

```
curl http://localhost:8546/send_tx -d "uid=0&to=0x123"
curl http://localhost:8546/send_tx -d "uid=1&to=0x123"
curl http://localhost:8546/send_tx -d "uid=2&to=0x123"
curl localhost:8546/owner/1
curl localhost:8546/owner/2
curl localhost:8546/owner/3
curl localhost:8546/owner/0
curl localhost:8546/coins/0x123
```
