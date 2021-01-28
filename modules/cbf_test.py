import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings; warnings.filterwarnings('ignore')


def recommend_places(data_file_path, place_id):
    pd.set_option('display.max_columns', 70)                       # 출력할 열의 최대개수
    pd.set_option('display.max_colwidth', 80)                      # 출력할 열의 너비
    review_matrix = pd.read_csv(data_file_path)
    tag_list = []

    for i in range(len(review_matrix)):

        count_table = pd.DataFrame(review_matrix.iloc[i,5:])
        count_table = count_table.sort_values(by =[i], ascending = False)
        count_table = count_table[count_table[i] != 0]

        if len(count_table) >= 7:
            count_table = count_table.iloc[:7,:]
            count_table_list = count_table.index.to_list()
        else : count_table_list = count_table.index.to_list()

        tag_list.append(count_table_list)

    review_matrix['tag_list'] = tag_list
    cbf_matrix = review_matrix[['id','place','tag_list']]
    cbf_matrix['tag_list_literal'] = cbf_matrix['tag_list'].apply(lambda x : (' ').join(x))
    count_vect = CountVectorizer(min_df=0, ngram_range=(1, 2))
    tag_matrix = count_vect.fit_transform(cbf_matrix['tag_list_literal'])
    tag_sim = cosine_similarity(tag_matrix, tag_matrix)
    tag_sim_sorted_ind = tag_sim.argsort()[:, ::-1]

    index = review_matrix[review_matrix['id'] == place_id].index.values.astype(int)[0]
    index_list = tag_sim_sorted_ind[index][0:21]

    review_matrix_dict = review_matrix[['id','place']].to_dict('records')
    place_list = []
    for index in index_list:
        place_list.append(review_matrix_dict[index])
    return place_list


def get_places_id_place(data_file_path):
    place_list = pd.read_csv(data_file_path)
    return place_list[['id', 'place']].to_dict('records')