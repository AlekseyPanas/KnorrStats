from enum import IntEnum
import Constants as c
import datetime
import threading
import time
import Globe
import pygame
import math
import requests
import Button
import Game


class App:

    class State(IntEnum):
        MAIN = 0
        EDIT = 1

    def __init__(self):
        # State Machine bois
        self.state = App.State.MAIN

        # List of Game Data objects
        self.GAMES = []
        self.GAME_EDITING = None

        self.daily_player_data = None

        # Gets today's date and renders it
        self.date = datetime.date.today()
        self.date_text = None
        self.set_date_text()

        # Various static texts that will need to be displayed on screen
        self.txt1 = c.get_rockwell_font(c.cscale(45)).render("Date:", True, c.Colors.BLACK.value)
        self.txt2 = c.get_rockwell_font(c.cscale(40)).render("New", True, c.Colors.DARK_GREEN.value)

        # Player names, ids, and main roster info retrieved from database
        self.raw_player_json = None

        # Map IDs along with their string names
        self.raw_map_json = None

        # >>> Main State Buttons
        self.add_date_button = Button.Button(c.cscale(400, 13), c.cscale(30, 30), c.add_button_image)
        self.sub_date_button = Button.Button(c.cscale(400, 56), c.cscale(30, 30), c.subtract_button_image)
        self.new_game_button = Button.Button(c.cscale(835, 28), c.cscale(40, 40), c.new_button_image)

        """Stuff Related to loading"""
        # Flag which halts all states and runs loading screen
        self.loading = False

        self.retry_button = Button.Button(c.cscale(375, 445), c.cscale(150, 48), c.retry_button_image)

        # Function to run on thread followed by the thread object
        self.thread_target = lambda x: x
        self.load_thread = threading.Thread(target=self.__load)
        # Message to display while loading (must be a rendered pygame surface)
        self.rendered_message = None
        # If the thread_target throws an error in the other thread this variable will be populated
        self.error = None

        # Starts loading screen for player data
        self.loading = True
        self.rendered_message = c.get_code_font(c.cscale(50)).render("Retrieving Players...", False, c.Colors.BLACK.value)
        self.thread_target = Globe.SERV.setPlayerData
        self.load_thread.start()

    # Creates new thread object
    def reset_thread(self):
        self.load_thread = threading.Thread(target=self.__load)

    # Renders date as surface
    def set_date_text(self):
        self.date_text = c.get_rockwell_font(c.cscale(45)).render(self.date.strftime("%m/%d/%Y"), True, c.Colors.GRAY.value)

    # Runs app GUI
    def run_app(self, screen):
        if self.loading:
            self.run_loading_screen(screen)
        else:
            # Runs states
            if self.state == App.State.MAIN:
                self.run_main_state(screen)
            elif self.state == App.State.EDIT:
                self.run_edit_state(screen)

    """>>> App States:"""
    def run_main_state(self, screen):
        # Draws background
        screen.blit(c.bg_image, (0, 0))

        # Draws date text
        screen.blit(self.txt1, c.cscale(20, 20))
        screen.blit(self.date_text, c.cscale(160, 20))

        # Draws date add/subtract buttons
        self.add_date_button.draw(screen)
        self.add_date_button.is_hover(pygame.mouse.get_pos())
        self.sub_date_button.draw(screen)
        self.sub_date_button.is_hover(pygame.mouse.get_pos())

        # Draws 'New' text
        screen.blit(self.txt2, self.txt2.get_rect(center=c.cscale(790, 50)))

        # Draws new game button
        self.new_game_button.draw(screen)
        self.new_game_button.is_hover(pygame.mouse.get_pos())

        # Event handler
        for event in Globe.events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Checks button presses and acts accordingly
                    if self.add_date_button.is_clicked(event.pos):
                        # Adds 1 day to date
                        self.date += datetime.timedelta(days=1)
                        self.set_date_text()

                    elif self.sub_date_button.is_clicked(event.pos):
                        # Subtracts 1 day from date
                        self.date -= datetime.timedelta(days=1)
                        self.set_date_text()

                    elif self.new_game_button.is_clicked(event.pos):
                        # Adds blank new game
                        self.GAMES.append(Game.GameData(self.raw_player_json))

        # Runs each game's menu GUI
        for idx in range(len(self.GAMES)):
            self.GAMES[idx].run_game_menu(screen, 165 + (80 * idx))

            # Checks if game was selected for editing
            if self.GAMES[idx].edit:
                # Resets edit flag
                self.GAMES[idx].edit = False
                # Sets state
                self.state = self.State.EDIT
                # Points to game being edited
                self.GAME_EDITING = self.GAMES[idx]

        # Removes dead games
        self.GAMES = [game for game in self.GAMES if not game.kill]

    def run_edit_state(self, screen):
        screen.fill(c.Colors.LIGHT_BLUE.value)

        self.GAME_EDITING.run_game_edit(screen)
    """<<<"""

    def run_loading_screen(self, screen):
        # Nice blue color
        screen.fill(c.Colors.LIGHT_BLUE.value)

        # Loads while there is no error
        if self.error is None:
            # Creates moving animation for the swords using sin function
            screen.blit(c.sword_loading_image,
                        c.sword_loading_image.get_rect(center=c.cscale(450 + (50 * math.sin(5*time.time())), 400)))
            screen.blit(pygame.transform.flip(c.sword_loading_image, True, False),
                        c.sword_loading_image.get_rect(center=c.cscale(450 - (50 * math.sin(5*time.time())), 470)))

            # Draws rendered message below
            screen.blit(self.rendered_message, self.rendered_message.get_rect(center=c.cscale(450, 550)))

        # If an error is set, creates a retry screen
        else:
            # Draws error text
            error_text = c.get_code_font(c.cscale(50)).render(self.error, False, c.Colors.MAROON.value)
            screen.blit(error_text, error_text.get_rect(center=c.cscale(450, 550)))

            # Draws button
            self.retry_button.draw(screen)
            self.retry_button.is_hover(pygame.mouse.get_pos())

            # Button Event
            for event in Globe.events:
                if event.type == pygame.MOUSEBUTTONUP:
                    # Left Mouse button
                    if event.button == 1:
                        # If retry button is pressed
                        if self.retry_button.is_clicked(event.pos):
                            # Removes error and restarts
                            self.error = None
                            self.reset_thread()
                            self.load_thread.start()

    def __load(self):
        try:
            self.thread_target()
        except requests.exceptions.ConnectionError:
            self.error = "Failed to load: Server offline"
        except Exception as e:
            self.error = "Failed to load: Something went wrong"

        # Loading will not end if an error is found. It is the job of the loading screen GUI
        # to handle retrying on the loading screen.
        if self.error is None:
            self.loading = False
