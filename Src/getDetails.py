import os
from pathlib import Path
import sqlite3


db_path = Path(os.path.dirname(os.path.dirname(__file__))) / 'data' / 'app_list.db'
getDetails_URL = "https://store.steampowered.com/app/"
#Steam 正在了解该游戏 game_area_details_specs_ctn learning_about

def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT appid FROM apps WHERE status = 1")


main()
