# -*- coding: UTF-8 -*-
from datetime import datetime
import json

class Chat:
    def __init__(self):
        pass

    def getTime(self):
        now = datetime.now()
        return json.dumps({"plugin": "chat","method": "getTime", \
                           "body": now.strftime("Il est %HH%M")})