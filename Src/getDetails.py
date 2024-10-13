import os
import sqlite3
from pathlib import Path

import requests
import urllib3
from bs4 import BeautifulSoup

db_path = Path(os.path.dirname(os.path.dirname(__file__))) / 'data' / 'app_list.db'
getDetails_URL = "https://store.steampowered.com/app/"
cookie = {'mature_content': '1', 'birthtime': '441734400', 'lastagecheckage': '1-January-1900',
          'Steam_Language': 'english', 'bShouldUseHTML5': '1'}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    rows = cursor.execute("SELECT appid FROM apps WHERE status = 1").fetchall()
    for row in rows:
        check(row[0],cursor)
        conn.commit()
    conn.close()


def check(appid,cursor):

    url = f"{getDetails_URL}{appid}"
    html_response = requests.get(url, allow_redirects=False, verify=False, cookies=cookie)

    # 检查是否重定向到 store.steampowered.com 被BAN游戏受限
    if 'Location' in html_response.headers and 'store.steampowered.com' in html_response.headers['Location']:
        print(f"appid {appid}无有效商店页面")
        cursor.execute("UPDATE apps SET status = 3 WHERE appid = ?", (appid,))
        return

    html_text = html_response.text
    soup = BeautifulSoup(html_text, 'html.parser')
    div = soup.find('div', class_='game_area_details_specs_ctn learning_about')

    if div:
        label_div = div.find('div', class_='label') # type: ignore
        if label_div and 'Profile Features Limited' in label_div.text:
            print(f"appid {appid}受限")
            cursor.execute("UPDATE apps SET status = 2 WHERE appid = ?", (appid,))
        else:
            print(f"appid {appid}仍处于了解状态")
            cursor.execute("UPDATE apps SET status = 1 WHERE appid = ?", (appid,))
    else:
        print(f"appid {appid}未受限")
        cursor.execute("UPDATE apps SET status = 0 WHERE appid = ?", (appid,))

main()

