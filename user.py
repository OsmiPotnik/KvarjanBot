__author__ = 'Mark'

import urllib.request
import json


url = "https://api.twitch.tv/kraken/channels/"
game = ""


def return_game(channel):
    request = urllib.request.Request(url + channel)
    response = urllib.request.urlopen(request)
    data = json.loads(response.read().decode('utf-8'))
    if data["game"] is None:
        return "Game undifined"
    else:
        return data["game"]
