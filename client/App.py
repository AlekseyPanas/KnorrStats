from enum import IntEnum
import Constants as c
import datetime


class App:

    class State(IntEnum):
        MAIN = 0

    def __init__(self):
        self.state = App.State.MAIN

        self.date = datetime.date.today()
        self.date_text = None
        self.set_date_text()

        self.txt1 = c.get_rockwell_font(c.cscale(45)).render("Date:", True, c.Colors.BLACK.value)

    def set_date_text(self):
        self.date_text = c.get_rockwell_font(c.cscale(45)).render(self.date.strftime("%m/%d/%Y"), True, c.Colors.GRAY.value)

    def run_app(self, screen):
        if self.state == App.State.MAIN:
            self.run_main_state(screen)

    def run_main_state(self, screen):
        screen.blit(c.bg_image, (0, 0))

        screen.blit(self.txt1, c.cscale(20, 20))
        screen.blit(self.date_text, c.cscale(160, 20))
