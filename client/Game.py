import pygame
import Constants as c
import Button
import Typefield
import Globe
import ChoiceSelector
import copy


# Data storage class for each game played
class GameData:
    def __init__(self, player_json):
        # TODO: Add Map Name and score display on game tab in main menu
        # GUI
        self.edit_button = Button.Button(list(c.cscale(570, 0)), c.cscale(128, 33), c.edit_button_image)
        self.delete_button = Button.Button(list(c.cscale(720, 0)), c.cscale(128, 33), c.delete_button_image)

        # Edit GUI
        self.back_button = Button.Button(c.cscale(15, 15), c.cscale(128, 40), c.back_button_image)
        self.left_button = Button.Button(c.cscale(15, 440), c.cscale(45, 45), c.arrow_button_image)
        self.right_button = Button.Button(c.cscale(840, 440), c.cscale(45, 45),
                                          pygame.transform.flip(c.arrow_button_image, True, False))
        self.map_left_button = Button.Button(c.cscale(330, 25), c.cscale(20, 20), c.arrow_button_image)
        self.map_right_button = Button.Button(c.cscale(360, 25), c.cscale(20, 20),
                                              pygame.transform.flip(c.arrow_button_image, True, False))

        # Flag to remove game from list
        self.kill = False
        # Flag to determine if edit was pressed
        self.edit = False

        # Map information
        self.map_idx = 0
        self.map_id = Globe.APP.raw_map_json[self.map_idx % len(Globe.APP.raw_map_json)]["map_id"]
        self.map_name = Globe.APP.raw_map_json[self.map_idx % len(Globe.APP.raw_map_json)]["map_name"]
        self.map_name_surf = c.get_rockwell_font(c.cscale(35)).render(self.map_name, True, c.Colors.GRAY.value)

        # Display text
        self.txt1 = c.get_rockwell_font(c.cscale(25)).render("Team Rounds:", False, c.Colors.BLACK.value)
        self.txt2 = c.get_rockwell_font(c.cscale(25)).render("Enemy Rounds:", False, c.Colors.BLACK.value)
        self.txt3 = c.get_rockwell_font(c.cscale(25)).render("Reason:", False, c.Colors.BLACK.value)
        self.txt4 = c.get_rockwell_font(c.cscale(25)).render("Commendation:", False, c.Colors.BLACK.value)
        self.txt5 = c.get_rockwell_font(c.cscale(25)).render("Criticism:", False, c.Colors.BLACK.value)
        self.txt6 = c.get_rockwell_font(c.cscale(25)).render("Is Excused?:", False, c.Colors.BLACK.value)
        self.txt7 = c.get_rockwell_font(c.cscale(25)).render("Has Notified?:", False, c.Colors.BLACK.value)
        self.txt8 = c.get_rockwell_font(c.cscale(35)).render("Score: ", False, c.Colors.BLACK.value)
        self.txt9 = c.get_rockwell_font(c.cscale(35)).render("Map: ", False, c.Colors.BLACK.value)

        # Form fields for data entry
        self.typefields = [Typefield.Field(c.cscale(570, 20), c.cscale(60), c.get_rockwell_font(c.cscale(20)),
                                           c.typefield_image, allowed_symbols=("0", "1", "2", "3", "4", "5", "6",
                                                                               "7", "8", "9"),
                                           field_id="team_rounds"),
                           Typefield.Field(c.cscale(800, 20), c.cscale(60), c.get_rockwell_font(c.cscale(20)),
                                           c.typefield_image, allowed_symbols=("0", "1", "2", "3", "4", "5", "6",
                                                                               "7", "8", "9"),
                                           field_id="enemy_rounds")]

        # Variables which are updated once 'BACK' is pressed. Used for score display in menu
        self.enemy_rounds_val = ""
        self.team_rounds_val = ""

        # PlayerData objects for each player
        self.player_data = [PlayerGameData(player["player_id"]) for player in Globe.APP.raw_player_json]
        # Player Page
        self.page = 0

        # Current PlayerGameData object based on page
        self.current_player_data = self.player_data[self.page % len(self.player_data)]
        # Current PlayerDailyData object based on player ID
        self.daily_player_data = [player for player in Globe.APP.daily_player_data if player.player_id == self.current_player_data.player_id][0]
        # Combined field array
        self.combined_fields = self.typefields + self.current_player_data.typefields + self.daily_player_data.typefields

    def run_game_edit(self, screen):
        # Draws text
        screen.blit(self.txt1, self.txt1.get_rect(center=c.cscale(500, 35)))
        screen.blit(self.txt2, self.txt2.get_rect(center=c.cscale(720, 35)))
        screen.blit(self.txt3, self.txt3.get_rect(center=c.cscale(495, 670)))
        screen.blit(self.txt3, self.txt3.get_rect(center=c.cscale(495, 740)))
        screen.blit(self.txt4, self.txt4.get_rect(center=c.cscale(180, 670)))
        screen.blit(self.txt5, self.txt5.get_rect(center=c.cscale(230, 740)))
        screen.blit(self.txt6, self.txt6.get_rect(center=c.cscale(230, 810)))
        if self.daily_player_data.notif_selector is not None:
            screen.blit(self.txt7, self.txt7.get_rect(center=c.cscale(580, 810)))

        # Blits map name
        screen.blit(self.map_name_surf, self.map_name_surf.get_rect(center=c.cscale(240, 35)))

        # Draws player name
        player_name = c.getPlayerFromJson(self.current_player_data.player_id, Globe.APP.raw_player_json)["player_name"]
        rendered_name = c.get_rockwell_font(c.cscale(60)).render(player_name, True, c.Colors.BLACK.value)
        screen.blit(rendered_name, rendered_name.get_rect(center=c.cscale(450, 200)))

        # Draws text for player page
        for txt in self.current_player_data.txtlist:
            screen.blit(txt["surf"], txt["pos"])

        # Draws field
        for field in self.combined_fields:
            field.draw_handler(screen)

        # Runs buttons
        self.back_button.draw(screen)
        self.left_button.draw(screen)
        self.right_button.draw(screen)
        self.map_left_button.draw(screen)
        self.map_right_button.draw(screen)

        self.back_button.is_hover(pygame.mouse.get_pos())
        self.left_button.is_hover(pygame.mouse.get_pos())
        self.right_button.is_hover(pygame.mouse.get_pos())
        self.map_left_button.is_hover(pygame.mouse.get_pos())
        self.map_right_button.is_hover(pygame.mouse.get_pos())

        # Runs ChoiceSelectors
        self.current_player_data.isabsent.draw_handler(screen)
        self.daily_player_data.commend_selector.draw_handler(screen)
        self.daily_player_data.criticism_selector.draw_handler(screen)
        self.daily_player_data.excuse_selector.draw_handler(screen)
        if self.daily_player_data.notif_selector is not None:
            self.daily_player_data.notif_selector.draw_handler(screen)

        # Event handling
        for event in Globe.events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Back Button
                    if self.back_button.is_clicked(event.pos):
                        # Updates score variables
                        self.enemy_rounds_val = [field.text for field in self.typefields if field.field_id == "enemy_rounds"][0]
                        self.team_rounds_val = [field.text for field in self.typefields if field.field_id == "team_rounds"][0]
                        # Resets state
                        self.edit = False
                        Globe.APP.state = Globe.APP.State.MAIN

                    # Left Arrow Button
                    elif self.left_button.is_clicked(event.pos):
                        # Removes page
                        self.page -= 1
                        if self.page < 0:
                            self.page = len(self.player_data) - 1
                        # Resets fields and variables
                        self.current_player_data = self.player_data[self.page % len(self.player_data)]
                        self.daily_player_data = [player for player in Globe.APP.daily_player_data if
                                                  player.player_id == self.current_player_data.player_id][0]
                        self.combined_fields = self.typefields + self.current_player_data.typefields + self.daily_player_data.typefields

                    # Right Arrow Button
                    elif self.right_button.is_clicked(event.pos):
                        # Adds page
                        self.page += 1
                        # Resets fields and variables
                        self.current_player_data = self.player_data[self.page % len(self.player_data)]
                        self.daily_player_data = [player for player in Globe.APP.daily_player_data if
                                                  player.player_id == self.current_player_data.player_id][0]
                        self.combined_fields = self.typefields + self.current_player_data.typefields + self.daily_player_data.typefields

                    # Map Cycle buttons
                    elif self.map_left_button.is_clicked(event.pos):
                        # Shifts index
                        self.map_idx -= 1
                        if self.map_idx < 0:
                            self.map_idx = len(Globe.APP.raw_map_json) - 1
                        # Resets values
                        self.map_id = Globe.APP.raw_map_json[self.map_idx % len(Globe.APP.raw_map_json)]["map_id"]
                        self.map_name = Globe.APP.raw_map_json[self.map_idx % len(Globe.APP.raw_map_json)]["map_name"]
                        self.map_name_surf = c.get_rockwell_font(c.cscale(35)).render(self.map_name, True,
                                                                                      c.Colors.GRAY.value)

                    elif self.map_right_button.is_clicked(event.pos):
                        # Shifts index
                        self.map_idx += 1
                        # Resets values
                        self.map_id = Globe.APP.raw_map_json[self.map_idx % len(Globe.APP.raw_map_json)]["map_id"]
                        self.map_name = Globe.APP.raw_map_json[self.map_idx % len(Globe.APP.raw_map_json)]["map_name"]
                        self.map_name_surf = c.get_rockwell_font(c.cscale(35)).render(self.map_name, True,
                                                                                      c.Colors.GRAY.value)

            if event.type == pygame.KEYUP:
                # Tabs through fields
                if event.key == pygame.K_TAB:
                    selected_field = [field for field in self.combined_fields if field.selected]
                    if len(selected_field):
                        # Deselects old field
                        selected_field[0].selected = False
                        # Selects next field in the list
                        self.combined_fields[(self.combined_fields.index(selected_field[0]) + 1) % len(self.combined_fields)].selected = True
                    else:
                        # If nothing was selected, select first
                        self.combined_fields[0].selected = True

            # Runs ChoiceSelectors
            self.current_player_data.isabsent.event_handler(event)
            self.daily_player_data.commend_selector.event_handler(event)
            self.daily_player_data.criticism_selector.event_handler(event)
            self.daily_player_data.excuse_selector.event_handler(event)
            if self.daily_player_data.notif_selector is not None:
                self.daily_player_data.notif_selector.event_handler(event)

            # Fields for main game info
            for field in self.combined_fields:
                field.event_handler(event)

    def run_game_menu(self, screen, y_center):
        # Sets button height
        self.edit_button.top_left[1] = c.cscale(y_center - 15)
        self.delete_button.top_left[1] = c.cscale(y_center - 15)

        # Draw tab background image
        screen.blit(c.tab_image, c.tab_image.get_rect(center=c.cscale(450, y_center)))

        # Draws display text (score + Map)
        screen.blit(self.txt8, self.txt8.get_rect(center=c.cscale(100, y_center)))
        screen.blit(self.txt9, self.txt9.get_rect(center=c.cscale(350, y_center)))

        # Displays score
        if self.team_rounds_val == "" or self.enemy_rounds_val == "":
            score_color = c.Colors.LIGHT_GRAY.value
        elif int(self.team_rounds_val) < int(self.enemy_rounds_val):
            score_color = c.Colors.RED.value
        elif int(self.team_rounds_val) == int(self.enemy_rounds_val):
            score_color = c.Colors.YELLOW.value
        else:
            score_color = c.Colors.GREEN.value
        screen.blit(c.get_rockwell_font(c.cscale(30)).render(self.team_rounds_val + "-" + self.enemy_rounds_val,
                                                             True, score_color),
                    c.cscale(150, y_center - 15))
        # Displays MAP
        screen.blit(c.get_rockwell_font(c.cscale(30)).render(self.map_name, True, c.Colors.LIGHT_GRAY.value),
                    c.cscale(410, y_center - 15))

        # Draws buttons
        self.edit_button.draw(screen)
        self.edit_button.is_hover(pygame.mouse.get_pos())
        self.delete_button.draw(screen)
        self.delete_button.is_hover(pygame.mouse.get_pos())

        # Events Handler
        for event in Globe.events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.edit_button.is_clicked(event.pos):
                        self.edit = True

                    elif self.delete_button.is_clicked(event.pos):
                        self.kill = True


class PlayerGameData:
    def __init__(self, player_id):
        self.player_id = player_id

        field_ids = (
            "kills",
            "assists",
            "score",
            "mvps",
            "adr",
            "hs",
            "ud",
            "ef",
            "3ks",
            "4ks",
            "5ks",
            "score_pos",
            "kill_pos",
        )

        # >>> Creates list of typefields and texts for each data entry
        self.typefields = []
        self.txtlist = []

        # Reference pos for type field positioning
        pos = [250, 300]

        for idx in range(len(field_ids)):
            text_width = c.get_rockwell_font(25).render(field_ids[idx], False, c.Colors.GRAY.value).get_width()

            # Position Adjustment
            if pos[0] + text_width + 80 > 650:
                pos[0] = 250
                pos[1] += 40

            # Saves text position and surface
            self.txtlist.append({
                "pos": copy.copy(c.cscale(*pos)),
                "surf": c.get_rockwell_font(c.cscale(25)).render(field_ids[idx], False, c.Colors.GRAY.value)
            })

            # Position shift
            pos[0] += text_width + 10

            # Adds typefield
            self.typefields.append(Typefield.Field(c.cscale(*pos), c.cscale(60), c.get_rockwell_font(c.cscale(20)),
                                                   c.typefield_image, allowed_symbols=("0", "1", "2", "3", "4", "5",
                                                                                       "6", "7", "8", "9"),
                                                   field_id=field_ids[idx], player_id=player_id))

            # Position shift
            pos[0] += 70

        self.txtlist.append({
            "pos": c.cscale(330, pos[1] + 40),
            "surf": c.get_rockwell_font(c.cscale(25)).render("is absent?", False, c.Colors.GRAY.value)
        })

        # Chooser object for is_absent flag
        self.isabsent = ChoiceSelector.Chooser(c.cscale(20, 20), c.yes_image, c.no_image, c.cscale(470, pos[1] + 53))


class PlayerDailyData:
    def __init__(self, player_id):
        self.player_id = player_id

        # Form fields for data entry
        self.typefields = [Typefield.Field(c.cscale(550, 650), c.cscale(300), c.get_rockwell_font(c.cscale(20)),
                                           c.typefield_image, field_id="commend_reason"),
                           Typefield.Field(c.cscale(550, 720), c.cscale(300), c.get_rockwell_font(c.cscale(20)),
                                           c.typefield_image, field_id="criticism_reason")]

        # Selectors for daily data
        self.commend_selector = ChoiceSelector.Chooser(c.cscale(20, 20), c.yes_image, c.no_image, c.cscale(300, 670))
        self.criticism_selector = ChoiceSelector.Chooser(c.cscale(20, 20), c.yes_image, c.no_image, c.cscale(300, 740))

        self.excuse_selector = ChoiceSelector.Chooser(c.cscale(20, 20), c.yes_image, c.no_image, c.cscale(325, 810))
        # Selector for notification before game start time, only for main roster
        self.notif_selector = None
        if c.getPlayerFromJson(self.player_id, Globe.APP.raw_player_json)["is_main_roster"]:
            self.notif_selector = ChoiceSelector.Chooser(c.cscale(20, 20), c.yes_image, c.no_image, c.cscale(700, 810))
