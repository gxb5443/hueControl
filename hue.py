from pprint import pprint
import requests
import json
import ssdp
from urllib.parse import urlparse
import time

class hueApp(object):
    def __init__(self, name="", ip="", user=""):
        self.name = name
        self.ip = ip
        self.user = user
        self.setup()

    def setup(self):
        print("Setting up..")
        if self.ip == "":
            r = ssdp.discover("upnp:rootdevice")
            self.ip = next(urlparse(x.location).netloc[:-3] for x in r if "IpBridge" in x.server)
        self.getLights()
        self.getGroups()

    def getGroups(self):
        groups= requests.get("http://{ip}/api/{user}/groups".format(**self.__dict__))
        self.groups=groups.json()
        #for k,v in self.groups:
        #    self.groupMap[v['name']]=k

    def setGroupState(self, id, attr, val):
        payload = { attr: val }
        return requests.put("http://{}/api/{}/groups/{}/state".format(self.ip, self.user, id), json=payload).json()

    def getLights(self):
        lights = requests.get("http://{ip}/api/{user}/lights".format(**self.__dict__))
        self.lights=lights.json()
        #for k,v in self.lights:
        #    self.lightMap[v['name']]=k

    def getLightState(self, id):
        return requests.get("http://{}/api/{}/lights/{}".format(self.ip, self.user, id)).json()

    def setLightState(self, id, attr, val):
        payload = { attr: val }
        return requests.put("http://{}/api/{}/lights/{}/state".format(self.ip, self.user, id), json=payload).json()

    def off(self, id):
        self.setLightState(id, "on", False)

    def on(self, id):
        self.setLightState(id, "on", True)

    def setLightBrightness(self, id, brightness):
        self.setLightState(id, "bri", brightness)

if __name__=='__main__':
    a = hueApp("myApp", "192.168.1.180", "aFLDsKnNUbWJiHQ3NY7Z9BMG-leUsddbcpMKdFDi")
    for i in range(1,10):
        a.on(str(i))
        a.setLightState(str(i), "sat", 240)
        a.setLightBrightness(str(i), 125)
    time.sleep(10)
    for i in range(1,10):
        a.off(str(i))
