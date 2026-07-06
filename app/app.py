from ui.main_window import MusicPlayerUI
from app.controller import Controller
from core.player import MusicPlayer
from core.playlist import PlayList


class App:
    def __init__(self):
        self.player = MusicPlayer()
        self.playlist = PlayList()

        self.controller = Controller(self.player, self.playlist)

        # controller → UI
        self.ui = MusicPlayerUI(self.controller)

        # UI → controller
        self.controller.set_ui(self.ui)

    def run(self):
        self.ui.mainloop()
