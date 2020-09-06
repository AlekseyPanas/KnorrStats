import requests as req
import Globe
import time
import Game
import Constants as c


class DataMissing(Exception):
    pass


class UploadFailedException(Exception):
    pass


class NoDatabaseException(Exception):
    pass


class ServerComms:
    def __init__(self, domain_addr: str):
        # the main address of the page (ie: "google.com", "pornhub.com")
        self.domain_addr = domain_addr
        # Final json to upload to database
        self.uploadJSON = None

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

        # Checks if server returned an error object
        if (type(Globe.APP.raw_player_json) == dict and list(Globe.APP.raw_player_json.keys())[0] == "error") or (
                type(Globe.APP.raw_map_json) == dict and list(Globe.APP.raw_map_json.keys())[0] == "error"):
            raise NoDatabaseException

        # Creates Daily Game Data objects for each player
        Globe.APP.daily_player_data = [Game.PlayerDailyData(player["player_id"]) for player in Globe.APP.raw_player_json]

    def submitData(self):
        # Creates final JSON object
        self.buildJSON()
        # Fake loading for authenticity
        time.sleep(1)

        Globe.APP.rendered_message = c.get_code_font(c.cscale(50)).render("Uploading Data...", False,
                                                                     c.Colors.BLACK.value)

        # Uploads JSON
        output = req.post("http://127.0.0.1:3000/ajax/upload_data", json=self.uploadJSON).json()

        # If for whatever reason the server gives a fail response
        if not output["success"]:
            raise UploadFailedException

        # More fake loading
        time.sleep(1)

    def buildJSON(self):
        if not len(Globe.APP.GAMES):
            raise DataMissing

        # Gets daily player data
        player_daily = []
        for player in Globe.APP.daily_player_data:
            commend_reason = c.getTypeField("commend_reason", player.typefields).text
            crit_reason = c.getTypeField("criticism_reason", player.typefields).text
            # Checks if commend or crit field is missing a reason when it should have one
            if (commend_reason == "" and player.commend_selector.state) or (crit_reason == "" and player.criticism_selector.state):
                raise DataMissing

            if c.getPlayerFromJson(player.player_id, Globe.APP.raw_player_json)["is_main_roster"]:
                has_notif = player.notif_selector.state
            else:
                has_notif = None

            player_daily.append({
                "player_id": player.player_id,
                "date": Globe.APP.date.strftime("%m/%d/%Y"),
                "is_commend": player.commend_selector.state,
                "commend_reason": commend_reason,
                "is_criticism": player.criticism_selector.state,
                "criticism_reason": crit_reason,
                "is_excused": player.excuse_selector.state,
                "has_notified": has_notif
            })

        # Builds game json
        games = []
        for game in Globe.APP.GAMES:
            # Whaaat? No score?
            if game.enemy_rounds_val == "" or game.team_rounds_val == "":
                raise DataMissing

            players_data_list = []
            for plyr in game.player_data:
                player_json = {
                    "player_id": plyr.player_id,
                    "isabsent": plyr.isabsent.state
                }

                # Adds all field entries to json and checks if any field is missing
                for field in plyr.typefields:
                    if plyr.isabsent.state:
                        val = None
                    else:
                        try:
                            val = int(field.text)
                        except ValueError:
                            raise DataMissing

                    player_json[field.field_id] = val

                players_data_list.append(player_json)

            game_json = {
                "date": Globe.APP.date.strftime("%m/%d/%Y"),
                "map_id": game.map_id,
                "team_rounds": game.team_rounds_val,
                "enemy_rounds": game.enemy_rounds_val,
                "player_data": players_data_list
            }

            games.append(game_json)

        # Final JSON object
        self.uploadJSON = {
            "games": games,
            "player_daily": player_daily
        }
