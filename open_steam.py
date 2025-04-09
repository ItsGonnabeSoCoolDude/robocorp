from robocorp.tasks import task
from RPA.Desktop import Desktop
import os

@task
def search_top_games():
    open_steam_client()

def open_steam_client():
    # Define the Steam path (Windows-style path if possible)
    STEAM_PATH="/mnt/c/Program Files (x86)/Steam/steam.exe"

    # Verify the file exists
    if not os.path.exists(STEAM_PATH):
        print(f"Steam executable not found at: {STEAM_PATH}")
        return

    # Try to open Steam
    desktop = Desktop()
    try:
        desktop.open_application(STEAM_PATH)
        print("Steam opened successfully!")
    except Exception as e:
        print(f"Failed to open Steam: {e}")