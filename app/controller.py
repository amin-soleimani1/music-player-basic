import sys, os


class Controller:
    def __init__(self, player, playlist):
        self.player = player
        self.playlist = playlist
        self.ui = None

    def set_ui(self, ui):
        self.ui = ui

    # for relative path images
    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    # ---------------- Events from UI ----------------

    def on_select_music(self, filename):
        self.player._unlock = True
        self.ui.real_time.set(0)
        self.player.play(filename)
        metadata = self.playlist.get_metadata(filename)

        self.ui.update_title(metadata["title"])
        self.ui.update_artwork(metadata["artwork"])
        self.ui.update_play_button(True)

        self.get_current_time()
        self.get_music_time_len(filename)

    def on_play_pause(self):
        paused = self.player.pause_unpause()
        self.ui.update_play_button(not paused)

    def on_stop(self):
        self.player._unlock = False
        self.ui.real_time.set(0)
        self.ui.state_var.set(0)
        self.player.stop()
        self.ui.reset_ui()
        if self.ui.get_selected_index():
            self.ui.unselect_listbox(self.ui.get_selected_index())
        else:
            pass

    def on_volume(self, vol):
        self.player.set_volume(vol)

    def on_next(self):
        files = self.playlist.all_files()
        current = self.ui.get_selected_index()
        if current is None:
            return

        next_index = self.player.next_index(current, len(files) - 1)
        self.ui.select_listbox(next_index)
        self.on_select_music(files[next_index])

    def on_previous(self):
        files = self.playlist.all_files()
        current = self.ui.get_selected_index()
        if current is None:
            return

        prev_index = self.player.previous_index(current)
        self.ui.select_listbox(prev_index)
        self.on_select_music(files[prev_index])

    def on_add_music(self):
        if self.player.busy():
            selected_index = self.ui.get_selected_index()
            self.player.pause()
            self.playlist.add()
            self.ui.refresh_playlist(self.playlist.all_files())
            self.ui.select_listbox(selected_index)
        elif self.player._for_add_button == True:
            selected_index = self.ui.get_selected_index()
            self.playlist.add()
            self.ui.refresh_playlist(self.playlist.all_files())
            self.ui.select_listbox(selected_index)
        else:
            self.playlist.add()
            self.ui.refresh_playlist(self.playlist.all_files())

    def remove_music(self):
        if self.ui.get_selected_index():
            new_music = self.ui.get_selected_index() - 1
            self.player.stop()
            self.playlist.remove(self.ui.get_selected_name())
            self.ui.refresh_playlist(self.playlist.all_files())
            self.ui.select_listbox(new_music)
        else:
            pass

    def on_time_slider(self, state):
        if self.player._unlock:
            self.ui.real_time.set(state)
            if self.ui.get_selected_name() is not None:
                if self.player._paused_on_slaider:
                    self.player.set_volume(1)
                    self.player.play(self.ui.get_selected_name(), state)
                else:
                    self.player.set_volume(0)
                    self.player.play(self.ui.get_selected_name(), state)
                    self.player.pause()
            else:
                pass
        else:
            pass

    def get_current_time(self):
        current_time = self.ui.real_time.get() + self.player.get_pg_postion()
        self.ui.update_lab_current(self.player.str_f_time(current_time))
        self.ui.state_var.set(current_time)
        if current_time + 1 == self.ui.music_len.get():
            if self.ui.get_selected_index() + 1 < self.ui.size():
                self.ui.select_listbox(self.ui.get_selected_index() + 1)
            else:
                self.ui.select_listbox(0)
        self.ui.after(1000, self.get_current_time)

    def get_music_time_len(self, file_name):
        mp3_len = self.playlist.get_metadata(file_name)
        length = mp3_len["length"]
        self.ui.music_len.set(length)
        self.ui.update_lab_time_len(self.player.str_f_time(length))
        self.ui.update_slider_to(length)

    # ------------------ Events Key From UI --------------------

    def on_key(self, event):
        if event.keysym == "space":
            self.on_play_pause()
        elif event.keysym == "Right":
            self.on_next()
        elif event.keysym == "Left":
            self.on_previous()
        elif event.keysym == "Delete":
            self.remove_music()
        elif event.keysym == "Escape":
            self.ui.destroy()
