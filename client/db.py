import requests as req
import Globe
import time
import Game
import Constants as c


class DataMissing(Exception):
    pass


class ServerComms:
    def __init__(self, domain_addr: str):
        # the main address of the page (ie: "google.com", "pornhub.com")
        self.domain_addr = domain_addr

    def getLink(self, path: str):
        # Returns the response from the requested path (ie: "/faggotinfo/gays")
        return req.get(self.domain_addr + path)

    def setPlayerData(self):
        # Delay for debugging
        time.sleep(2)

        # Sets raw player json to data from server
        Globe.APP.raw_player_json = req.get(self.domain_addr + "/ajax/getplayers").json()

        # As an additional function, loads map data from database
        Globe.APP.raw_map_json = req.get(self.domain_addr + "/ajax/getmaps").json()

        # Creates Daily Game Data objects for each player
        Globe.APP.daily_player_data = [Game.PlayerDailyData(player["player_id"]) for player in Globe.APP.raw_player_json]

    def submitData(self):
        self.buildJSON()

        Globe.APP.rendered_message = c.get_code_font(c.cscale(50)).render("Uploading Data...", False,
                                                                     c.Colors.BLACK.value)

        time.sleep(2)

    def buildJSON(self):
        time.sleep(2)
        # raise DataMissing
