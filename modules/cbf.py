import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval
import warnings; warnings.filterwarnings('ignore')


def recommend_places(data_for_service, data_place_index_list):
    pd.set_option('display.max_columns', 70)  # 출력할 열의 최대개수
    pd.set_option('display.max_colwidth', 80)  # 출력할 열의 너비
    # 필요한 데이터 불러오기
    data1 = pd.read_csv(data_for_service)
    sim_order_table = pd.read_csv(data_place_index_list)

    keyword = ['자연', '가족', '아이', '휴식', '여유']
    weight = [10, 5, 5, 4, 3]

    user_data = pd.DataFrame({'keyword': keyword, 'weight': weight})
    user_data['rate'] = user_data['weight'] / (sum(user_data['weight']))
    user_data = user_data.sort_values('rate', ascending=False)
    user_data = user_data.reset_index()

    # 가상 장소 확정 짓기 (키워드 별로 뽑기)
    keyword_order = list(user_data['keyword'])
    print(keyword_order)

    # 키워드가 들어간 장소는 다 뽑기(쉬운 모델링을 위해 상위 3개만 고려함....)
    firstword_table = data1[data1['tag_list'].str.contains(keyword_order[0])]
    secondword_table = data1[data1['tag_list'].str.contains(keyword_order[1])]
    thirdword_table = data1[data1['tag_list'].str.contains(keyword_order[2])]

    entire_table = pd.concat([firstword_table, secondword_table, thirdword_table], axis=0)
    entire_table = entire_table.drop_duplicates()

    if len(entire_table) >= 100:
        next_table = firstword_table
    else:
        next_table = entire_table

    # 한 번 걸러진,next_table에서 우선순위 단어 고려해보기
    A1 = next_table[next_table['first_tag'] == keyword_order[0]]
    A2 = next_table[next_table['second_tag'] == keyword_order[0]]
    A3 = next_table[next_table['third_tag'] == keyword_order[0]]
    important_A = pd.concat([A1, A2, A3])
    important_A = important_A.drop_duplicates()

    if len(next_table) >= 50:
        semi_table = A1
    elif len(next_table) >= 20:
        semi_table = important_A
    else:
        semi_table = next_table

    B1 = semi_table[semi_table['first_tag'] == keyword_order[1]]
    B2 = semi_table[semi_table['second_tag'] == keyword_order[1]]
    B3 = semi_table[semi_table['third_tag'] == keyword_order[1]]
    B4 = semi_table[semi_table['fourth_tag'] == keyword_order[1]]
    B5 = semi_table[semi_table['fifth_tag'] == keyword_order[1]]

    important_B = pd.concat([B1, B2, B3, B4, B5])
    important_B = important_B.drop_duplicates()

    if len(semi_table) >= 30:
        if len(important_B[(important_B['first_tag'] == keyword_order[0]) & (
                important_B['second_tag'] == keyword_order[1])]) >= 1:
            final_table = important_B[
                (important_B['first_tag'] == keyword_order[0]) & (important_B['second_tag'] == keyword_order[1])]
        else:
            final_table = important_B[
                (important_B['first_tag'] == keyword_order[0]) | (important_B['second_tag'] == keyword_order[1])]
    elif len(semi_table) >= 20:
        final_table = important_B[important_B['first_tag'] == keyword_order[0]]
    else:
        final_table = semi_table

    # 최종 spot 선정
    # '투어' 들어간 데이터 제외시키기
    tour_table = final_table[final_table['place'].str.contains('투어')]
    tour_table_index = tour_table.index.to_list()
    final_table = final_table.drop(tour_table_index, axis=0)

    if len(final_table) >= 2:
        end_table = final_table.sort_values('count', ascending=False).iloc[:3, :]
    else:
        end_table = final_table
    entire_table = pd.concat([firstword_table, secondword_table, thirdword_table], axis=0)

    return None


def get_places_id_place(data_file_path):
    place_list = pd.read_csv(data_file_path)
    return place_list[['id', 'place']].to_dict('records')