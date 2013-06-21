from rivescript import rivescript

failed_response = "I don't know what to say"
rivescript_failed_responses = set(["ERR: No Reply Found" , "ERR: No Reply Matched", "ERR: Error when executing Python object"])

class RiveScriptBot():
    def respond_to(self, text, user="localuser"):
        response = self.k.reply(user,text)
        if response in rivescript_failed_responses:
            response = failed_response
        return response

    def learn(self, filefoldername):
        self.k.load_directory(filefoldername)
        self.k.sort_replies()

    def __init__(self):
        self.k = rivescript.RiveScript(utf8=True)
