import sqlite3
from modules.common import *
from ast import literal_eval

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


def get_photo_data_by_id(sqlite_path, photo_id):
    print(photo_id)
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, tags FROM photos WHERE id = ?;", [photo_id])
    rows = cursor.fetchall()
    photo = {'id': rows[0][0], 'tags': rows[0][2]}
    cursor.close()
    conn.close()
    return photo


def get_tag_data(sqlite_path, photo_id_list):
    tag_data = {}
    for photo_id in photo_id_list:
        photo = get_photo_data_by_id(sqlite_path, str(photo_id))
        print(photo['tags'])
        print(type(literal_eval(photo['tags'])))
    return tag_data