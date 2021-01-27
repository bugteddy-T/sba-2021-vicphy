import pandas as pd


def get_places(data_file_path):
    places = pd.read_excel(data_file_path)
    return places.to_dict('records')


def get_place_by_id(data_file_path, id):
    places = pd.read_excel(data_file_path)
    place = places.query("id == " + str(id)).to_dict('records')[0]
    return place