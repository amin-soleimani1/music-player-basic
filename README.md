# 🎵 Music Player Basic

> 📌 Part of the Music Engineering Journey
> https://github.com/amin-soleimani1/music-engineering-journey

A simple desktop music player built with Python and CustomTkinter.

🌐 **Language:** English | [فارسی](README.fa.md)

## Phase 1 — Desktop Application Fundamentals

A desktop music player built with **Python** and **CustomTkinter**.

This project is the first phase of my Music Engineering Journey. Its primary goal was to learn the fundamentals of Python desktop application development, GUI design, project organization, and audio playback.

### 🔗 Project Navigation

⬅️ **Previous Phase**  
None

➡️ **Next Phase**  
[Music Library Manager](https://github.com/amin-soleimani1/Music-Library-Manager.git/blob/main/README.md)

> **Note**
>
> This is an educational project created to practice Python programming and desktop application development. It is not intended to be a production-ready music player.

---

# Preview

### Main Interface

<p align="center">
  <img src="assets/images/application_gif3.gif" width="900"/>
</p>

---

# Features

## 🎵 Music Playback

- Play local music files
- Play / Pause controls
- Previous / Next track
- Playlist support

## 🖼 Album Artwork

- Display embedded album artwork
- Default artwork when no cover image is available

## 🖥 User Interface

- Desktop interface built with CustomTkinter
- Simple and clean layout
- Basic music player controls

---

# Technologies

- Python
- CustomTkinter
- CTkListbox
- pygame
- Pillow
- music_tag

---

# Project Structure

The project follows a simple modular structure to separate the application's user interface, playback logic, and resources.

```text
Music Player Basic/
│
├── main.py                  # Application entry point
│
├── app/                     # Application layer
│   ├── app.py               # Application initialization
│   └── controllers.py       # Application controllers
│
├── core/                    # Core playback logic
│   ├── player.py            # Audio playback engine
│   └── playlist.py          # Playlist management
│
├── ui/                      # User interface
│   └── main_window.py       # Main application window
│
├── assets/                  # Static resources
│   ├── icons/               # Application icons
│   └── images/              # Album artwork and UI images
│
└── music_files/             # Sample music directory
```

---

# What I Learned

This project helped me learn:

- Python desktop development
- GUI programming with CustomTkinter
- Audio playback using pygame
- Project organization
- File handling
- Playlist management

This project laid the foundation for the next phase of the journey, where I redesigned the application using a database, improved architecture, and cleaner project organization.

---

# Requirements

- Python 3.10+ (tested on Python 3.10, 3.11 and 3.12)

---

# Installation & Run

Clone the repository:

```bash
git clone https://github.com/amin-soleimani1/music-player-basic.git
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

---

# Build Executable (Optional)

```bash
pyinstaller --onefile --windowed main.py
```

---

# Next Step

The next project in this journey expands this application by introducing:

- SQLite database
- Better project architecture
- Improved user experience
- Refactoring
- Better code organization

➡️ Music Library Manager

---

This repository is published for educational purposes.

Feel free to explore the source code and use it as a learning resource.
