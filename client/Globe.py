import pygame
import App
import db

APP = None
SERV = None
events = None
running = True


def start_app():
    global APP, SERV, events
    SERV = db.ServerComms("http://127.0.0.1:3000")
    APP = App.App()

    events = pygame.event.get()
