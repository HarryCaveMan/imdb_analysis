import pandas as pd
from file_utils import *
import os
DATA_PATH = test_data_path = os.path.abspath('../../../../data/movie_metadata.csv')

def read_file(filename:str,return_type:str='dataframe'):
    file:FileHandler = FileHandler(filename)
    return file.get_data(return_type=return_type)    

def calculate_top_marginal_roi(data_frame,colname:str,top_n:int=10):
    lookup_cols = ['gross','budget']
    lookup_cols.extend(colnames)
    if(set(lookup_cols).intersection(set(data_frame.columns)) != lookup_cols):
        raise Error(f"Required columns {' '.join(lookup_cols)} not in input data")
    sub_frame = movies[lookup_cols].groupby(colnames).sum()
    sub_frame['marginal_roi'] = (sub_frame['gross'] - sub_frame['budget'])/sub_frame['budget']
    return sub_frame.nlargest(top_n,'marginal_roi')

def calculate_top_gross_profit(data_frame,colnames:list,top_n:int=10,metric:str='sum'):
    lookup_cols = ['gross','budget']
    lookup_cols.extend(colnames)
    if(metric=='sum'):
        sub_frame = data_frame[lookup_cols].groupby(colnames).sum()
        sub_frame['gross_profit'] = sub_frame['gross'] - sub_frame['budget']
    if(metric=='mean'):
        data_frame['gross_profit'] = data_frame['gross'] - data_frame['budget']
        lookup_cols.append('gross_profit')
        sub_frame = data_frame[lookup_cols].groupby(colnames).mean()    
    return sub_frame.nlargest(top_n,'gross_profit')

def union_actor_columns(movies):
    sub_frame = movies[['actor_1_name','actor_2_name','actor_3_name','budget','gross']]
    actor_1 = sub_frame[['actor_1_name','budget','gross']].rename(columns={'actor_1_name':'actor_name'})
    actor_2 = sub_frame[['actor_2_name','budget','gross']].rename(columns={'actor_2_name':'actor_name'})
    actor_3 = sub_frame[['actor_3_name','budget','gross']].rename(columns={'actor_3_name':'actor_name'}) 
    return pd.concat([actor_1,actor_2,actor_3])

def main():
    movies = read_file(DATA_PATH)
    top_10_genres_avg = calculate_top_gross_profit(data_frame=movies,colnames=['genres'],metric='mean')
    top_10_genres_total = calculate_top_gross_profit(data_frame=movies,colnames=['genres'])
    # A lot of movies had zero budget, so marginal roi is not a good metric
    #grouped_aggregated_genres_marginal = calculate_top_marginal_roi(movies=movies,colname='genres')
    # print(top_10_genres)
    # print(grouped_aggregated_genres_marginal)
    #no not for collective baragaing xD
    #there are 3 actor columns, so I union them into a single col
    actors_union = union_actor_columns(movies)
    top_10_actors_avg = calculate_top_gross_profit(data_frame=actors_union,colnames=['actor_name'],metric='mean')
    top_10_actors_total = calculate_top_gross_profit(data_frame=actors_union,colnames=['actor_name'])

    print(top_10_actors_avg)
    print(top_10_actors_total)

    


if __name__ == '__main__':
    main()