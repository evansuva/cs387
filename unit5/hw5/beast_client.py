import urllib
import json
import base64

BLOCK_SIZE = 128
site = "http://mintchocolatechip.local:8080/tls"

def unencode_json(txt):
    d = json.loads(txt)
    return dict((str(k),
                 base64.urlsafe_b64decode(str(v)))
                for k,v in d.iteritems())

def _send(attack=None, token=None):
    data = {}
    if attack is not None:
        data["attack"] = base64.urlsafe_b64encode(attack)
    if token is not None:
        data["token"] = base64.urlsafe_b64encode(token)

    json = urllib.urlopen(site, urllib.urlencode(data)).read()
    json = unencode_json(json)
    return json
    

_TOKEN = None
def send(attack=None):
    global _TOKEN
    json = _send(attack, _TOKEN)
    _TOKEN = json["token"]
    return json["message"]

