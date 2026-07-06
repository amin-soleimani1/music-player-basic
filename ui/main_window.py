import customtkinter
from PIL import Image
from io import BytesIO
import os
import CTkListbox
import tkinter


class MusicPlayerUI(customtkinter.CTk):
    def __init__(self, controller):
        super().__init__(fg_color="black")

        self.controller = controller
        self.real_time = tkinter.IntVar(value=0)
        self.state_var = tkinter.IntVar(value=0)
        self.music_len = tkinter.IntVar(value=0)

        self.title("Music Player")
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.geometry(f"{self.width}x{self.height}-8+-8")

        self.build_ui()
        self.refresh_playlist(self.get_all_files())
        self.bind("<Key>", self.controller.on_key)

    # ---------------- UI Construction ----------------

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2), weight=0)

        # -------- ( ARTWORK ) --------
        artwork = customtkinter.CTkFrame(
            self,
            fg_color="#070707",
            bg_color="black",
            border_width=1,
            border_color="#252525",
        )
        artwork.grid(column=0, row=0, pady=(10, 0), padx=(35, 25), sticky="nsew")
        artwork.grid_columnconfigure((0, 2), weight=1)
        artwork.grid_columnconfigure(1, weight=0)
        artwork.grid_rowconfigure(0, weight=0)
        artwork.grid_rowconfigure(1, weight=1)

        # Artwork
        self.default_art = customtkinter.CTkImage(
            Image.open(self.controller.resource_path("assets/images/artwork.jpg")),
            size=(480, 480),
        )
        self.art_label = customtkinter.CTkLabel(
            artwork,
            text="",
            image=self.default_art,
        )
        self.art_label.grid(column=1, row=1)

        # Title
        self.title_label = customtkinter.CTkLabel(
            artwork,
            text="Music Name",
            font=customtkinter.CTkFont(
                family="Baskerville Old Face", size=35, weight="bold"
            ),
        )
        self.title_label.grid(column=1, row=0, pady=(30, 0), sticky="ew")

        # -------- ( CONTROLS ) --------
        buttons = customtkinter.CTkFrame(self, height=110, fg_color="transparent")
        buttons.grid(column=0, row=2, pady=(0, 15), padx=10, sticky="nsew")
        buttons.grid_columnconfigure((0, 6), weight=1)
        buttons.grid_columnconfigure(([i for i in range(1, 6)]), weight=0)
        buttons.grid_rowconfigure(0, weight=1)

        self.play_icon = customtkinter.CTkImage(
            Image.open(self.controller.resource_path("assets/icons/start_dark.png")),
            size=(80, 80),
        )
        self.pause_icon = customtkinter.CTkImage(
            Image.open(self.controller.resource_path("assets/icons/stop_dark.png")),
            size=(80, 80),
        )
        self.next_icon = customtkinter.CTkImage(
            Image.open(self.controller.resource_path("assets/icons/right_light.png")),
            size=(60, 60),
        )
        self.prev_icon = customtkinter.CTkImage(
            Image.open(self.controller.resource_path("assets/icons/left_light.png")),
            size=(60, 60),
        )

        self.play_button = customtkinter.CTkButton(
            buttons,
            width=10,
            height=10,
            text="",
            bg_color="transparent",
            fg_color="transparent",
            image=self.pause_icon,
            hover_color="#252525",
            command=self.controller.on_play_pause,
        )
        self.play_button.grid(column=3, row=0, padx=20)

        customtkinter.CTkButton(
            buttons,
            width=10,
            height=10,
            text="",
            bg_color="transparent",
            fg_color="transparent",
            image=self.prev_icon,
            hover_color="#252525",
            command=self.controller.on_previous,
        ).grid(column=2, row=0, padx=20)

        customtkinter.CTkButton(
            buttons,
            width=10,
            height=10,
            text="",
            bg_color="transparent",
            fg_color="transparent",
            image=self.next_icon,
            hover_color="#252525",
            command=self.controller.on_next,
        ).grid(column=4, row=0, padx=20)

        customtkinter.CTkButton(
            buttons,
            text="stop",
            width=120,
            height=14,
            fg_color="#070707",
            bg_color="black",
            border_width=1,
            border_color="#252525",
            hover_color="#252525",
            command=self.controller.on_stop,
        ).grid(column=1, row=0, padx=20)

        # Volume Slider
        self.volume_slider = customtkinter.CTkSlider(
            buttons,
            width=120,
            variable=tkinter.IntVar(value=1),
            command=self.controller.on_volume,
        )
        self.volume_slider.grid(column=5, row=0, padx=20)

        # -------- ( TIME SLAIDER ) -------
        slider = customtkinter.CTkFrame(self, height=50, fg_color="transparent")
        slider.grid(column=0, row=1, pady=10, padx=10, sticky="nsew")
        slider.grid_columnconfigure(1, weight=1)
        slider.grid_columnconfigure((0, 2), weight=0)
        slider.grid_rowconfigure(0, weight=1)

        # slider time
        self.slider_time = customtkinter.CTkSlider(
            slider,
            from_=0,
            to=100,
            variable=self.state_var,
            command=self.controller.on_time_slider,
        )
        self.slider_time.grid(column=1, row=0, sticky="ew")

        # current time lab
        self.lab_sli_current_time = customtkinter.CTkLabel(slider, text="00:00")
        self.lab_sli_current_time.grid(column=0, row=0, padx=(40, 0), sticky="nsew")

        # time len lab
        self.lab_sli_time_len = customtkinter.CTkLabel(slider, text="00:00")
        self.lab_sli_time_len.grid(column=2, row=0, padx=(0, 40), sticky="nsew")

        # -------- ( PLAYLIST ) --------
        sidebar = customtkinter.CTkFrame(self, width=250, fg_color="transparent")
        sidebar.grid(column=1, row=0, rowspan=3, pady=10, padx=10, sticky="nsew")
        sidebar.grid_columnconfigure(0, weight=1)
        sidebar.grid_rowconfigure(1, weight=1)
        sidebar.grid_rowconfigure((0, 2, 3, 4), weight=0)

        customtkinter.CTkLabel(
            sidebar,
            text=("Play List"),
            font=customtkinter.CTkFont(
                family="Baskerville Old Face", size=25, weight="bold"
            ),
        ).grid(column=0, row=0, pady=(10, 0))

        self.listbox = CTkListbox.CTkListbox(
            sidebar,
            width=200,
            border_width=1,
            fg_color="#070707",
            bg_color="black",
            highlight_color="#353535",
            border_color="#252525",
            hover_color="#151515",
            command=self.on_click_list,
        )
        self.listbox.grid(column=0, row=1, padx=10, pady=15, sticky="nsew")

        customtkinter.CTkLabel(
            sidebar,
            text="-----------------------------------------------------------",
            text_color="#404040",
        ).grid(column=0, row=2, padx=10, pady=10, sticky="nsew")

        customtkinter.CTkButton(
            sidebar,
            text="add music",
            width=220,
            height=35,
            fg_color="#070707",
            bg_color="black",
            border_width=1,
            border_color="#252525",
            hover_color="#252525",
            font=customtkinter.CTkFont(
                family="Baskerville Old Face", size=25, weight="bold"
            ),
            command=self.controller.on_add_music,
        ).grid(column=0, row=3, padx=10, pady=(15, 20))

        customtkinter.CTkButton(
            sidebar,
            text="remove music",
            width=220,
            height=35,
            fg_color="#070707",
            bg_color="black",
            border_width=1,
            border_color="#252525",
            hover_color="#252525",
            font=customtkinter.CTkFont(
                family="Baskerville Old Face", size=25, weight="bold"
            ),
            command=self.controller.remove_music,
        ).grid(column=0, row=4, padx=10, pady=(0, 25))

    # ---------------- UI Event methods ----------------

    def on_click_list(self, filename):
        self.controller.on_select_music(filename)

    # ---------------- UI Update methods ----------------

    # Artwork and Title
    def update_title(self, name):
        self.title_label.configure(text=name)

    def update_artwork(self, raw_bytes):
        if raw_bytes:
            img = Image.open(BytesIO(raw_bytes))
            img = customtkinter.CTkImage(img, size=(480, 480))
            self.art_label.configure(image=img)
            self.art_label.image = img
        else:
            self.art_label.configure(image=self.default_art)

    # Button Play
    def update_play_button(self, playing: bool):
        self.play_button.configure(image=self.play_icon if playing else self.pause_icon)

    # Reset UI
    def reset_ui(self):
        self.update_title("Music Name")
        self.update_artwork(None)
        self.update_play_button(False)
        self.update_lab_current("00:00")
        self.update_lab_time_len("00:00")

    # Slider Time

    def update_slider_to(self, intger):
        self.slider_time.configure(to=intger)

    def update_lab_current(self, new_text):
        self.lab_sli_current_time.configure(text=new_text)

    def update_lab_time_len(self, new_text):
        self.lab_sli_time_len.configure(text=new_text)

    # ---------------- Playlist helpers ----------------

    def refresh_playlist(self, files):
        self.listbox.delete(0, "end")
        for f in files:
            self.listbox.insert("end", f)

    def get_all_files(self):
        try:
            return os.listdir("music_files")
        except:
            return []

    def get_selected_index(self):
        return self.listbox.curselection()

    def select_listbox(self, idx):
        self.listbox.activate(idx)

    def unselect_listbox(self, idx):
        self.listbox.deactivate(idx)

    def get_selected_name(self):
        return self.listbox.get(self.listbox.curselection())

    def size(self):
        return self.listbox.size()
