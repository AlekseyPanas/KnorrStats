import pygame
import App

APP = None
events = None
running = True


def start_app():
    global APP, events
    APP = App.App()

    events = pygame.event.get()
