import json
import threading

import requests
import websocket

from .exceptions import RequestFailedException


class AggregatorClient(object):

    def __init__(self, base_url, ws_url, verify=False, timeout=5):
        self.base_url = base_url
        self.verify = verify
        self.timeout = timeout

    #     self.ws = websocket.WebSocketApp(ws_url, on_message=self.ws_on_message)
    #     self.ws_callback = {}
    #     threading.Thread(target=self.ws.run_forever).start()

    # def ws_on_message(self, ws, message):
    #     data = json.loads(message)
    #     if callable(self.ws_callback[data['event']]):
    #         self.ws_callback[data['event']](data['arg'])

    # def emit(self, event, arg):
    #     self.ws.send(json.dumps({'event': event, 'arg': arg}, sort_keys=True))

    # def on(self, event, callback):
    #     self.ws_callback[event] = callback

    def request(self, end_point, method, params=None, data=None, headers=None):
        url = self.base_url + end_point

        response = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            verify=self.verify,
            timeout=self.timeout,
        )

        if response.ok:
            return response
        else:
            raise RequestFailedException(
                'failed reason: {}, text: {}'.format(
                    response.reason, response.text)
            )

    def get_owner(self, uid):
        end_point = f'/owner/{uid}'
        response = self.request(end_point, 'GET')
        return response.text

    def get_coins(self, owner):
        end_point = f'/coins/{owner}'
        response = self.request(end_point, 'GET')
        return response.text

    def get_proof(self, uid):
        end_point = f'/proof/{uid}'
        response = self.request(end_point, 'GET')
        return response.text

    def send_transaction(self, uid, to): # , sig):
        end_point = '/send_tx'
        data = {'uid': uid, 'to': to} #, 'sig': sig}
        response = self.request(end_point, 'POST', data=data)
        return response.text

    def submit_state(self):
        end_point = '/aggregator/submit_state'
        self.request(end_point, 'POST')
