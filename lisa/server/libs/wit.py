import requests

class Wit():
    def __init__(self, configuration):
        self.configuration = configuration
        self.failed_response = {"fr": "Je n'ai pas compris votre demande",
                   "en": "I didn't understood your question"
        }

    def message_send(self, text):
        headers = {'Authorization': 'Bearer ' + self.configuration['wit_token']}
        r = requests.get(self.configuration['wit_url'] + 'message', params={'q': text}, headers=headers)
        if r.ok:
            return r.json()

    def list_intents(self):
        headers = {'Authorization': 'Bearer ' + self.configuration['wit_token']}
        r = requests.get(self.configuration['wit_url'] + 'intents', headers=headers)
        if r.ok:
            return r.json()