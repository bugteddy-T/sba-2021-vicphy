import sqlite3
from modules.common import *


def get_photos(sqlite_path):
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, tags FROM photos")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    photo_list = []
    for row in rows:
        photo = {}
        photo['id'] = row[0]
        photo['filename'] = row[1]
        photo['tags'] = row[2]
        photo_list.append(photo)
    return get_random_list(photo_list)
