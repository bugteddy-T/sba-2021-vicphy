import pandas as pd
from modules.place import get_places_by_place_list, get_places_by_tour_type

def get_tour_type(user_data):
    # 여행자 상위 두 타입 고르기
    # def tour_type_1and2_with_weight(user_data):
    tour_type_Table = {"tour_type": ["Flex", "교양인", "놀래", "쉴래", "구경할래", "배울래"],
                       "sum_weight": [0, 0, 0, 0, 0, 0]}
    tour_type_Table = pd.DataFrame(tour_type_Table)
    flex = 0
    smart = 0
    hangout = 0
    rest = 0
    sightseeing = 0
    learning = 0
    for i in range(len(user_data)):
        key_text = user_data.iloc[i, 1]
        key_weight = user_data.iloc[i, 3]

        if key_text in '돈, 쇼핑, 시장, 싸다, 저렴하다, 비싸다,먹다,음식, 식사, 상품,구매':
            flex += key_weight
        if key_text in '박물관, 전시관,관광지,유적지,역사,유익하다,문화,궁전,전쟁':
            smart += key_weight
        if key_text == '미술관':
            smart += key_weight
        if key_text in '활동,놀이공원,게임,친구,커플,재미,아쿠아리움,엔터테인먼트,아이,가족,경기':
            hangout += key_weight
        if key_text in '힐링,공원,휴식,풍경,자연,전망대,산책,분수,여유,나들이':
            rest += key_weight
        if key_text in '공연,콘서트,이벤트,영화,예술,미술':
            sightseeing += key_weight
        if key_text in '강좌,요리,공예,체험':
            learning += key_weight
    tour_type_Table['sum_weight'] = [flex, smart, hangout, rest, sightseeing, learning]
    tour_type_Table = tour_type_Table.sort_values('sum_weight', ascending=False)
    tour_type_Table = tour_type_Table.reset_index()
    return tour_type_Table


def get_places_by_cbf(keyword, weight):
    data_cbf = {}
    pd.set_option('display.max_columns', 70)  # 출력할 열의 최대개수
    pd.set_option('display.max_colwidth', 80)
    # 출력할 열의 너비
    # 필요한 데이터 불러오기
    data1 = pd.read_csv('data/data-for-service-v.1.0.csv')
    data2 = pd.read_excel('data/place-data-v.1.3.xlsx')
    sim_order_table = pd.read_csv('data/place-index-list-by-cosine-similarity.csv')

    # 여행 키워드 단어와 가중치를 입력하시오!
    # 단 키워드 단어는
    # ['돈','쇼핑','시장','싸다, 저렴하다','비싸다','먹다','음식, 식사','상품','구매',
    # '가격','호텔','박물관','전시관','관광지','유적지','미술관','역사','유익하다','문화','궁전','전쟁','활동','놀이공원','게임',
    # '친구','커플','재미','아쿠아리움','엔터테인먼트','아이','가족','경기','힐링','공원','휴식','풍경','자연','전망대','산책',
    # '분수','여유','나들이','공연','콘서트','이벤트','영화','예술','미술','강좌','요리','공예','체험'] 중에서 선택해야한다.
    # 대략 5개의 키워드가 입력되었을 경우(실제로는 이렇게 안 되겠지만, 5개 상위 키워드로 뽑아서 진행할 것임)

    user_data = pd.DataFrame({'keyword': keyword, 'weight': weight})
    user_data['rate'] = user_data['weight'] / (sum(user_data['weight']))
    user_data = user_data.sort_values('rate', ascending=False)
    user_data = user_data.reset_index()
    # print(user_data)

    tour_type_Table = get_tour_type(user_data)
    data_cbf['tour_type'] = tour_type_Table.to_dict('records')

    try:
        first_user_tour_type = tour_type_Table.iloc[0, 1]
        first_user_tour_type_weight = float(tour_type_Table.iloc[0, 2]) * 100
        first_user_tour_type_num = tour_type_Table.iloc[0, 0] + 1
        second_user_tour_type = tour_type_Table.iloc[1, 1]
        second_user_tour_type_weight = float(tour_type_Table.iloc[1, 2]) * 100
        second_user_tour_type_num = tour_type_Table.iloc[1, 0] + 1
        thrid_user_tour_type_num = tour_type_Table.iloc[2, 0] + 1
        fourth_user_tour_type_num = tour_type_Table.iloc[3, 0] + 1

        user_info = [first_user_tour_type, first_user_tour_type_weight, first_user_tour_type_num,
                     second_user_tour_type, second_user_tour_type_weight, second_user_tour_type_num,
                     thrid_user_tour_type_num, fourth_user_tour_type_num]

        # 가상 장소 확정 짓기 (키워드 별로 뽑기)
        keyword_order = list(user_data['keyword'])
        # print(keyword_order)

        # 키워드가 들어간 장소는 다 뽑기(쉬운 모델링을 위해 상위 3개만 고려함....)
        firstword_table = data1[data1['tag_list'].str.contains(keyword_order[0])]
        secondword_table = data1[data1['tag_list'].str.contains(keyword_order[1])]
        thirdword_table = data1[data1['tag_list'].str.contains(keyword_order[2])]

        entire_table = pd.concat([firstword_table, secondword_table, thirdword_table], axis=0)
        entire_table = entire_table.drop_duplicates()
        # print('모으기')
        # print('entire_table 개수는 : ', len(entire_table))

        if len(entire_table) >= 100:
            next_table = firstword_table
        else:
            next_table = entire_table
        # print('next_table 개수는 : ', len(next_table))

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
        # print('semi_table 개수는 : ', len(semi_table))

        B1 = semi_table[semi_table['first_tag'] == keyword_order[1]]
        B2 = semi_table[semi_table['second_tag'] == keyword_order[1]]
        B3 = semi_table[semi_table['third_tag'] == keyword_order[1]]
        B4 = semi_table[semi_table['fourth_tag'] == keyword_order[1]]
        B5 = semi_table[semi_table['fifth_tag'] == keyword_order[1]]

        important_B = pd.concat([B1, B2, B3, B4, B5])
        important_B = important_B.drop_duplicates()

        if len(important_B) <= 5:
            final_table = semi_table
        elif len(semi_table) >= 30:
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
        # print('final_table 개수는 : ', len(final_table))

        # 최종 spot 선정
        # '투어' 들어간 데이터 제외시키기
        tour_table = final_table[final_table['place'].str.contains('투어')]
        tour_table_index = tour_table.index.to_list()
        final_table = final_table.drop(tour_table_index, axis=0)
        # print(final_table)

        if len(final_table) >= 2:
            end_table = final_table.sort_values('count', ascending=False).iloc[:3, :]
        else:
            end_table = final_table
        # 최종 spot 장소( 3개 이하)
        # print(end_table)
        # print(len(end_table))

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
        # print(virtual_place_name)
        # print(virtual_place_id)
        # print(virtual_place_index)

        # 각 장소 별 2군데 추가로 유사도로 선정

        recommend_id = []
        recommend_name = []
        recommend_index = []
        recommend_tourtype = []

        for i in range(3):
            recom = sim_order_table[sim_order_table['0'] == virtual_place_name[i]]
            spot1 = recom.iloc[0, 1]
            spot2 = recom.iloc[0, 2]
            spot3 = recom.iloc[0, 3]
            spot4 = recom.iloc[0, 4]
            spot5 = recom.iloc[0, 5]
            spot6 = recom.iloc[0, 6]
            spot7 = recom.iloc[0, 7]
            spot8 = recom.iloc[0, 8]
            spot9 = recom.iloc[0, 9]

            recommend_index.append(virtual_place_index[i])
            recommend_index.append(spot1)
            recommend_index.append(spot2)
            recommend_index.append(spot3)
            recommend_index.append(spot4)
            recommend_index.append(spot5)
            recommend_index.append(spot6)
            recommend_index.append(spot7)
            recommend_index.append(spot8)
            recommend_index.append(spot9)

        for j in recommend_index:
            find_name = sim_order_table.iloc[j, 0]
            recommend_name.append(find_name)

        for k in recommend_index:
            find_id = data1.iloc[k, 0]
            recommend_id.append(find_id)

        for t in recommend_id:
            find_type = list(data2[data2['id'] == t]['tour_type'])[0]
            recommend_tourtype.append(find_type)

        # print(recommend_index)
        # print(recommend_name)
        # print(recommend_id)
        # print(recommend_tourtype)

        # 최종 추천지 반환하기!!! (중복 당연히 제거)

        final_recommend_id = []
        final_recommend_name = []
        final_recommend_tourtype = []
        jungbok = []
        jungsang = []

        # 리뷰수가 5개 이상은 되는 곳으로!!
        for a in recommend_id:
            if data1[data1['id'] == a].iloc[0, 3] >= 5:
                final_recommend_id.append(a)

        # 중복제거를 위의 순서를 고려해서 하기!!(무작위 set안됨.)
        for b in final_recommend_id:
            if b in jungsang:
                jungbok.append(b)
            else:
                jungsang.append(b)

        for k in jungsang:
            final_name = data1[data1['id'] == k].iloc[0, 1]
            final_recommend_name.append(final_name)

        for k in jungsang:
            final_tourtype = list(data2[data2['id'] == k]['tour_type'])[0]
            final_recommend_tourtype.append(final_tourtype)

        # print("총 추천 결과는??")
        Recommendation_total = pd.DataFrame(
            {'id': jungsang, 'name': final_recommend_name, 'tour_type': final_recommend_tourtype})
        # RecommendationTotal 개수로 거르기

        if len(Recommendation_total) <= 10:
            f1 = data2[data2['tour_type'] == user_info[2]]
            f1 = f1[f1['tag_list'].str.contains(user_data.iloc[0, 1])].iloc[:5, :]
            final_table1 = f1[['id', 'place', 'tour_type']]
            f2 = data2[data2['tour_type'] == user_info[5]]
            f2 = f2[f2['tag_list'].str.contains(user_data.iloc[0, 1])].iloc[:5, :]
            final_table2 = f2[['id', 'place', 'tour_type']]

        # 상위 2개가 아닌 여행자 타입 구하기
        else:
            for_extra = list(set(Recommendation_total['tour_type'].to_list()))
            main = [user_info[2], user_info[5]]
            for_extra = [x for x in for_extra if x not in main]

            table1 = Recommendation_total[Recommendation_total['tour_type'] == user_info[2]]
            table2 = Recommendation_total[Recommendation_total['tour_type'] == user_info[5]]
            table3_extra = Recommendation_total[Recommendation_total['tour_type'] == for_extra[0]]
            table4_extra = Recommendation_total[Recommendation_total['tour_type'] == for_extra[1]]

            if len(table1) <= 4:
                plus_index = 4 - len(table1)
                plus = table3_extra.iloc[:int(plus_index) + 1, :]
                final_table1 = pd.concat([table1, plus])
                if len(final_table1) <= 4:
                    plus_index_e = 4 - len(final_table1)
                    plus_e = table4_extra.iloc[:int(plus_index_e) + 1, :]
                    final_table1 = pd.concat([final_table1, plus_e])
            else:
                final_table1 = table1.iloc[:5, :]

            if len(table2) <= 4:
                plus_index = 4 - len(table2)
                plus = table3_extra.iloc[:int(plus_index) + 1, :]
                final_table2 = pd.concat([table2, plus])
                if len(final_table2) <= 4:
                    plus_index_e = 4 - len(final_table2)
                    plus_e = table4_extra.iloc[:int(plus_index_e) + 1, :]
                    final_table2 = pd.concat([final_table2, plus_e])
            else:
                final_table2 = table2.iloc[:5, :]

        # print(tour_type_Table)
        # print(final_table1)
        # print(final_table2)
        places_data1 = get_places_by_place_list(final_table1.to_dict('records'))
        places_data2 = get_places_by_place_list(final_table2.to_dict('records'))

        data_cbf['places1'] = places_data1
        data_cbf['places2'] = places_data2
    except:
        print("except")
        type1_id = data_cbf['tour_type'][0]['index'] + 1
        type2_id = data_cbf['tour_type'][1]['index'] + 1
        print(type1_id)
        print(type2_id)
        places_data1 = get_places_by_tour_type(type1_id)
        places_data2 = get_places_by_tour_type(type2_id)
        data_cbf['places1'] = places_data1
        data_cbf['places2'] = places_data2
    finally:
        return data_cbf


def get_places_id_place(data_file_path):
    place_list = pd.read_csv(data_file_path)
    return place_list[['id', 'place']].to_dict('records')