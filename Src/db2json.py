from ast import For
from calendar import c
import json
import os
from pathlib import Path
import re
import sqlite3

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'app_list.db')
fulllist_file = Path(os.path.dirname(os.path.dirname(__file__))) / 'data' / 'fulllist.json'
normallist_file = Path(os.path.dirname(os.path.dirname(__file__))) / 'data' / 'normalist.json'
restrictedlist_file = Path(os.path.dirname(os.path.dirname(__file__))) / 'data' / 'restrictedlist.json'
learninglist_file = Path(os.path.dirname(os.path.dirname(__file__))) / 'data' / 'learninglist.json'
banlist_file = Path(os.path.dirname(os.path.dirname(__file__))) / 'data' / 'banlist.json'

restrictedandlearninglist_file = Path(os.path.dirname(os.path.dirname(__file__))) / 'data' / 'restrictedandlearninglist.json'

conn=sqlite3.connect(db_path)
cursor=conn.cursor()

# 查询所有正常状态的 appid
cursor.execute("SELECT appid FROM apps WHERE status = 0")
normallist = [row[0] for row in cursor.fetchall()]

with open(normallist_file, 'w', encoding='utf-8') as f:
    json.dump(normallist, f, ensure_ascii=False, indent=4)

# 查询所有受限状态的 appid
cursor.execute("SELECT appid FROM apps WHERE status = 2 OR status = 3")
restrictedlist = [row[0] for row in cursor.fetchall()]

with open(restrictedlist_file, 'w', encoding='utf-8') as f:
    json.dump(restrictedlist, f, ensure_ascii=False, indent=4)

# 查询所有了解状态的 appid
cursor.execute("SELECT appid FROM apps WHERE status = 1")
learninglist = [row[0] for row in cursor.fetchall()]

with open(learninglist_file, 'w', encoding='utf-8') as f:
    json.dump(learninglist, f, ensure_ascii=False, indent=4)

# 查询所有受限和了解状态的 appid
cursor.execute("SELECT * FROM apps WHERE status = 1 OR status = 2 OR status = 3")
restrictedandlearninglist = [row[0] for row in cursor.fetchall()]

with open(restrictedandlearninglist_file, 'w', encoding='utf-8') as f:
    json.dump(restrictedandlearninglist, f, ensure_ascii=False, indent=4)

# 查询所有无效状态的 appid
cursor.execute("SELECT * FROM apps WHERE status = 3")
banlist = [row[0] for row in cursor.fetchall()]

with open(banlist_file, 'w', encoding='utf-8') as f:
    json.dump(banlist, f, ensure_ascii=False, indent=4)

# 查询所有
cursor.execute("SELECT appid, status FROM apps")
fulllist = cursor.fetchall()

# 将查询结果转换为字典列表
fulllist_dict = [{"appid": row[0], "status": row[1]} for row in fulllist]

with open(fulllist_file, 'w', encoding='utf-8') as f:
    json.dump(fulllist_dict, f, ensure_ascii=False, indent=4)


conn.close()
