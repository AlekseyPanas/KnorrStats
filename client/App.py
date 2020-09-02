from enum import IntEnum
import Constants as c
import datetime
import threading
import time
import Globe
import pygame


class App:

    class State(IntEnum):
        MAIN = 0

    def __init__(self):
        # State Machine bois
        self.state = App.State.MAIN

        # Gets today's date and renders it
        self.date = datetime.date.today()
        self.date_text = None
        self.set_date_text()

        # Various static texts that will need to be displayed on screen
        self.txt1 = c.get_rockwell_font(c.cscale(45)).render("Date:", True, c.Colors.BLACK.value)

        # Player names, ids, and main roster info retrieved from database
        self.raw_player_json = None

        # Flag which halts all states and runs loading screen
        self.loading = False

        # Function to run on thread followed by the thread object
        self.thread_target = lambda x: x
        self.load_thread = threading.Thread(target=self.__load)
        # Message to display while loading
        self.load_message = ""
        # If the thread_target throws an error in the other thread this variable will be populated
        self.error = None

        # Starts loading screen for player data
        self.loading = True
        self.load_message = "Retrieving Players"
        self.thread_target = Globe.SERV.setPlayerData
        self.load_thread.start()

    def set_date_text(self):
        self.date_text = c.get_rockwell_font(c.cscale(45)).render(self.date.strftime("%m/%d/%Y"), True, c.Colors.GRAY.value)

    def run_app(self, screen):
        if self.loading:
            self.run_loading_screen(screen)
        else:
            # Runs states
            if self.state == App.State.MAIN:
                self.run_main_state(screen)

    def run_loading_screen(self, screen):
        # Nice blue color
        screen.fill((173, 216, 230))

        screen.blit(c.sword_loading_image, c.cscale(420, 400))
        screen.blit(pygame.transform.flip(c.sword_loading_image, False, True), c.cscale(420, 400))

    def run_main_state(self, screen):
        screen.blit(c.bg_image, (0, 0))

        screen.blit(self.txt1, c.cscale(20, 20))
        screen.blit(self.date_text, c.cscale(160, 20))

    def __load(self):
        try:
            self.thread_target()
        except Exception as e:
            self.error = e
        # TODO: Add more specific except statements to catch connection errors, etc

        # Loading will not end if an error is found. It is the job of the loading screen GUI
        # to handle retrying on the loading screen.
        if self.error is None:
            self.loading = False
