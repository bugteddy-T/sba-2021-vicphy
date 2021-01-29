import pandas as pd


def get_places():
    places = pd.read_excel('data/place-data-v.1.3.xlsx')
    return places.to_dict('records')


def get_place_by_id(id):
    places = pd.read_excel('data/place-data-v.1.3.xlsx')
    place = places.query("id == " + str(id)).to_dict('records')[0]
    return place


def get_places_by_tour_type(id):
    places = pd.read_excel('data/place-data-v.1.3.xlsx')
    count_review_min = 30
    query = "tour_type == " + str(id) + " and count_review > " + str(count_review_min)
    places = places.query(query)
    places = places.sort_values(["avg_review"], ascending=[False])
    places_dict = places.to_dict('records')
    return places_dict