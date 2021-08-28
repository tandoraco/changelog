import json

CALL_ZAPIER = False
CALL_WEBHOOK = False
CALL_TWITTER = False


class StaticResponseHandler:

    def __init__(self, path):
        self.path = path

    def get(self, key):
        response = {}
        with open(self.path, 'r') as f:
            response = json.loads(f.read())

        return response.get(key)
