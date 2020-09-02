import requests as req
import Globe
import time


class ServerComms:
    def __init__(self, domain_addr: str):
        # the main address of the page (ie: "google.com", "pornhub.com")
        self.domain_addr = domain_addr

    def getLink(self, path: str):
        # Returns the response from the requested path (ie: "/faggotinfo/gays")
        return req.get(self.domain_addr + path)

    def setPlayerData(self):
        # Delay for debugging
        time.sleep(20)

        # Sets raw player json to data from server
        Globe.APP.raw_player_json = req.get(self.domain_addr + "/ajax/getplayers").json()
