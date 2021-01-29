import sqlite3
from modules.common import *
from ast import literal_eval


def get_photos():
    conn = sqlite3.connect("static/data/photos.sqlite")
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


def get_photo_data_by_id(photo_id):
    print(photo_id)
    conn = sqlite3.connect("static/data/photos.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, tags FROM photos WHERE id = ?;", [photo_id])
    rows = cursor.fetchall()
    photo = {'id': rows[0][0], 'tags': rows[0][2]}
    cursor.close()
    conn.close()
    return photo


def get_tag_data(photo_id_list):
    tag_list = []
    for photo_id in photo_id_list:
        photo = get_photo_data_by_id(str(photo_id))
        tag_list.append(literal_eval(photo['tags']))
    tag_dict = {}
    for tag in tag_list:
        for key in tag:
            if tag_dict.get(key) is None:
                tag_dict[key] = tag[key]
            else:
                tag_dict[key] = tag_dict[key] + tag[key]
    tag_sorted = sorted(tag_dict.items(), key=(lambda x: x[1]), reverse=True)
    max = 5
    index = 1
    tag_data = {}
    for key, value in tag_sorted:
        tag_data[key] = value
        if index >= max:
            break
        index = index + 1
    return tag_data


'''
    type1 = ['돈', '쇼핑', '시장', '싸다, 저렴하다', '비싸다', '먹다', '음식, 식사', '상품', '구매', '가격', '호텔', ]
    type2 = ['박물관', '전시관', '관광지', '유적지', '미술관', '역사', '유익하다', '문화', '궁전', '전쟁']
    type3 = ['활동', '놀이공원', '게임', '친구', '커플', '재미', '아쿠아리움', '엔터테인먼트', '아이', '가족', '경기']
    type4 = ['힐링', '공원', '휴식', '풍경', '자연', '전망대', '산책', '분수', '여유', '나들이']
    type5 = ['공연', '콘서트', '이벤트', '영화', '예술', '미술']
    type6 = ['강좌', '요리', '공예', '체험']
https://pixabay.com/photos/dollars-currency-money-us-dollars-499481/ (FLEX) 1
https://pixabay.com/photos/museum-london-history-architecture-2203648/(교양인) 2
https://pixabay.com/photos/playground-swing-slide-school-fun-99509/(놀래) 3
https://pixabay.com/ko/photos/%EB%9C%A8%EA%B1%B0%EC%9A%B4-%EA%B3%B5%EA%B8%B0-%ED%92%8D%EC%84%A0-%EC%97%B4%EA%B8%B0%EA%B5%AC-%ED%92%8D%EC%84%A0-1149183/(쉴래) 4
https://pixabay.com/ko/photos/%EC%98%A4%ED%8E%98%EB%9D%BC-%EC%98%A4%EC%BC%80%EC%8A%A4%ED%8A%B8%EB%9D%BC-%EC%9D%8C%EC%95%85-594592/(구경할래) 5
https://pixabay.com/ko/photos/%EC%A0%90%ED%86%A0-%EB%8F%84%EC%9E%90%EA%B8%B0-%EC%86%90-%ED%8F%AC%ED%84%B0-1139098/(배울래) 6
'''
def get_tour_type_id(photo_id_list):
    tour_type = ["돈 쇼핑 시장 싸다 저렴하다 비싸다 먹다 음식 식사 상품 구매 가격 호텔", "박물관 전시관 관광지 유적지 미술관 역사 유익하다 문화 궁전 전쟁", "활동 놀이공원 게임 친구 커플 재미 아쿠아리움 엔터테인먼트 아이 가족 경기", "힐링 공원 휴식 풍경 자연 전망대 산책 분수 여유 나들이", "공연 콘서트 이벤트 영화 예술 미술", "강좌 요리 공예 체험"]
    tag_list = []
    for photo_id in photo_id_list:
        photo = get_photo_data_by_id(str(photo_id))
        tag_list.append(literal_eval(photo['tags']))
    tag_dict = {}
    for tag in tag_list:
        for key in tag:
            if tag_dict.get(key) is None:
                tag_dict[key] = tag[key]
            else:
                tag_dict[key] = tag_dict[key] + tag[key]
    tour_type_id_dict = {}
    for key in tag_dict:
        for index in range(len(tour_type)):
            type_id = index + 1
            if key in tour_type[index]:
                if tour_type_id_dict.get(str(type_id)) is None:
                    tour_type_id_dict[str(type_id)] = tag_dict[key]
                else:
                    tour_type_id_dict[str(type_id)] = tour_type_id_dict[str(type_id)] + tag_dict[key]
    tour_type_id_sorted = sorted(tour_type_id_dict.items(), key=(lambda x: x[1]), reverse=True)
    print(tour_type_id_sorted)
    tour_type_id_list = []
    for key, value in tour_type_id_sorted:
        tour_type_id_list.append(int(key))
    return tour_type_id_list

