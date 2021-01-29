import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval
import warnings; warnings.filterwarnings('ignore')


def get_places_by_cbf(tag_data):
    pd.set_option('display.max_columns', 70)  # 출력할 열의 최대개수
    pd.set_option('display.max_colwidth', 80)  # 출력할 열의 너비
    # 필요한 데이터 불러오기
    data1 = pd.read_csv('data/data-for-service.csv')
    sim_order_table = pd.read_csv('data/place-index-list-by-cosine-similarity.csv')

    keyword = []
    weight = []
    for key in tag_data:
        keyword.append(key)
        weight.append(tag_data[key])

    print(keyword)
    print(weight)

    user_data = pd.DataFrame({'keyword': keyword, 'weight': weight})
    user_data['rate'] = user_data['weight'] / (sum(user_data['weight']))
    user_data = user_data.sort_values('rate', ascending=False)
    user_data = user_data.reset_index()

    # 가상 장소 확정 짓기 (키워드 별로 뽑기)
    keyword_order = list(user_data['keyword'])

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
    # end_table이 완성이 되었다면, 여기서 1~3 개 정도의 spot을 가상으로 잡아, 유사도 높은 장소를 각가 2개씩 뽑아오기

    # 원래는 이 과정에서 여행 타입 별로 (비율적으로 분할해야한다...)
    virtual_place_name = []
    virtual_place_id = []
    virtual_place_index = end_table.index.to_list()

    for i in range(len(end_table)):
        vname = end_table.iloc[i, 1]
        vid = end_table.iloc[i, 0]
        virtual_place_name.append(vname)
        virtual_place_id.append(vid)

    # 각 장소 별 2군데 추가로 유사도로 선정

    recommend_id = []
    recommend_name = []
    recommend_index = []

    for i in range(10):
        recom = sim_order_table[sim_order_table['0'] == virtual_place_name[i]]
        spot1 = recom.iloc[0, 1]
        spot2 = recom.iloc[0, 2]
        recommend_index.append(virtual_place_index[i])
        recommend_index.append(spot1)
        recommend_index.append(spot2)

    for j in recommend_index:
        find_name = sim_order_table.iloc[j, 0]
        recommend_name.append(find_name)

    for k in recommend_index:
        find_id = data1.iloc[k, 0]
        recommend_id.append(find_id)

    # 최종 추천지 반환하기!!! (중복 당연히 제거)
    final_recommend_id = []
    final_recommend_name = []

    for a in recommend_id:
        if data1[data1['id'] == a].iloc[0, 3] >= 3:
            final_recommend_id.append(a)
    final_recommend_id = list(set(final_recommend_id))

    for k in final_recommend_id:
        final_name = data1[data1['id'] == k].iloc[0, 1]
        final_recommend_name.append(final_name)

    Recommendation = pd.DataFrame({'id': final_recommend_id, 'name': final_recommend_name})

    result_dict = Recommendation[['id','name']].to_dict('records')
    place_list = []
    for index in result_dict:
        place_list.append(result_dict[index])
    return place_list


def get_places_id_place(data_file_path):
    place_list = pd.read_csv(data_file_path)
    return place_list[['id', 'place']].to_dict('records')