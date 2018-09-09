import argparse

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from signer import create_app

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument('--host', default='127.0.0.1', help='Hostname to listen on.')
    parser.add_argument('--port', default='8547', help='Port number to listen on.')
    parser.add_argument('--identity', default='bob', help='Identity of user')
    args = parser.parse_args()

    app = create_app(identity=args.identity)

    print('Listening on ' + args.host + ':' + args.port)
    server = pywsgi.WSGIServer((args.host, int(args.port)), app, handler_class=WebSocketHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass