import pygame
import time


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self._paused = False  # for button pause & unpause
        self._unlock = False  # for button pause & unpause in quit state
        self._paused_on_slaider = True  # for slider on paused pygame state
        self._for_add_button = False  # for add button on paused pygame state

    def busy(self):
        return pygame.mixer.music.get_busy()

    def play(self, filename, start=None):
        pygame.mixer.init()
        pygame.mixer.music.load(f"music_files/{filename}")
        if not start == None:
            pygame.mixer.music.play(start=start)
        else:
            pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.quit()

    def pause(self):
        pygame.mixer.music.pause()

    def pause_unpause(self):
        if self._unlock:
            if self._paused:
                pygame.mixer.music.unpause()
                self.set_volume(1)
                self._paused_on_slaider = True
            else:
                pygame.mixer.music.pause()
                self._paused_on_slaider = False
                self._for_add_button = True

            self._paused = not self._paused
            return self._paused
        else:
            pass

    def set_volume(self, vol):
        pygame.mixer.music.set_volume(vol)

    def next_index(self, idx, max_idx):
        if idx >= max_idx:
            return 0
        return idx + 1

    def previous_index(self, idx):
        if idx <= 0:
            return 0
        return idx - 1

    def get_pg_postion(self):
        pygame.mixer.init()
        return int(pygame.mixer.music.get_pos() / 1000)

    def str_f_time(self, current):
        return time.strftime("%M:%S", time.gmtime(current))
