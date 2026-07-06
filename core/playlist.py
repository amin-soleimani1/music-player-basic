import sys, os
import shutil
import music_tag
from tkinter.filedialog import askopenfilename


class PlayList:
    def get_playlist_folder(self):
        if getattr(sys, "frozen", False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.getcwd()

        playlist_path = os.path.join(base_path, "music_files")

        if not os.path.exists(playlist_path):
            os.makedirs(playlist_path)

        return playlist_path

    def all_files(self):
        return os.listdir(self.get_playlist_folder())

    def get_metadata(self, filename):
        mp3 = music_tag.load_file(f"music_files/{filename}")
        return {
            "title": str(mp3["tracktitle"]),
            "artwork": mp3["artwork"].first.data if mp3["artwork"] else None,
            "length": int(mp3["#length"]),
        }

    def add(self):
        path = askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if path:
            shutil.copy(path, "music_files")

    def remove(self, music_name):
        os.remove(f"music_files/{music_name}")
