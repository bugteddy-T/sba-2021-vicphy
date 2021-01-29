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


def get_tour_type_data(tour_type_list):
    tour_type_text = ["FLEX", "교양", "놀기", "쉬기", "보기", "배우기"]
    tour_type_data = []
    for tour_type in tour_type_list:
        data = {}
        data['id'] = str(tour_type['index'] + 1)
        data['percent'] = str(int(tour_type['sum_weight'] * 100))
        tour_type['text'] = tour_type_text[tour_type['index']]
        tour_type_data.append(data)
    return tour_type_data


def get_places_by_place_list(place_list):
    places_data = []
    for place in place_list:
        id = place['id']
        places_data.append(get_place_by_id(id))
    return places_data