import json
import os
import sqlite3
import warnings
from pathlib import Path

import requests
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)

db_path = Path(os.path.dirname(os.path.dirname(__file__))) / 'data' / 'app_list.db'
getDetails_URL = "https://store.steampowered.com/api/appdetails?l=english&appids="
output_file = Path(os.path.dirname(os.path.dirname(__file__))) / 'data' / 'output.json'


def write_results_to_file(results):
    if output_file.exists():
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_results = json.load(f)
    else:
        existing_results = {}

    existing_results.update(results)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(existing_results, f, ensure_ascii=False, indent=4)


def update_status(conn, cursor, appid):
    cursor.execute("UPDATE apps SET status = true WHERE appid = ?", (appid,))
    conn.commit()


def check(appid, results, cursor, conn):
    url = f"{getDetails_URL}{appid}"
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        data = response.json()
        update_status(conn, cursor, appid)
        if data[str(appid)]['success']:
            app_data = data[str(appid)]['data']
            app_type = app_data.get('type', 'Unknown')
            results[appid] = app_type
            print(f"AppID: {appid}, 类型: {app_type}")
        else:
            print(f"获取appid: {appid}的详情失败")
    except requests.exceptions.RequestException as e:
        print(f"appid: {appid}的HTTP请求失败，错误: {e}")
        write_results_to_file(results)
        cursor.close()
        conn.close()
        exit(0)
    except ValueError as e:
        print(f"appid: {appid}的JSON解析失败，错误: {e}")


def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    rows = cursor.execute("SELECT appid FROM apps WHERE status = false").fetchall()
    results = {}

    for row in rows[:200]:
        appid = row[0]
        check(appid, results, cursor, conn)

    write_results_to_file(results)
    cursor.close()
    conn.close()


main()
