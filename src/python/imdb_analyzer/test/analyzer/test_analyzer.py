import os,sys
import pandas as pd
DATA_PATH = os.path.abspath('../../../../../data/movie_metadata.csv')
#insert analyzer package root
sys.path.insert(0,os.path.abspath('../../'))
from analyzer import *

#build small table I can hand calculate on to verify
TEST_COLUMN_NAMES = set({'actor_1_name','actor_2_name','actor_3_name','genres','budget','gross'})
TEST_COLUMNS = [
    ['Aaahnold','Lucille Ball','Aaahnold','Aaahnold','Vinnie Jones','Lucille Ball'],
    ['Lucille Ball','Aaahnold','Vinnie Jones','Lucille Ball','Aaahnold','Vinnie Jones'],
    # Just using a new actor (Mel Gibson) only on one row and setting this film's gross to zero 
    # This gives gives me three easy tests for my math functions:
    # Aaahnold and Vinnie MUST have lower averages than lucy, dragged down by Mel
    # Mel MUST be in last with zero gross
    # Lucy MUST be in first
    # having all other rows same just makes manual math easier on me for remaining tests
    ['Vinnie Jones','Vinnie Jones','Mel Gibson','Vinnie Jones','Lucille Ball','Aaahnold'],
    ['comedy','action','action','comedy','rom com','scifi'],
    [10,100,50,80,1000,0],
    # Set Mel gibsons row to zero gross
    [1000,10000,0,500,1500,10000]
]
test_df = pd.DataFrame(
    dict(zip(TEST_COLUMN_NAMES,TEST_COLUMNS))
)

def full_run():
    movies = read_file(DATA_PATH)
    top_10_genres_avg = calculate_top_gross_profit(data_frame=movies,colnames=['genres'],metric='mean')
    top_10_genres_total = calculate_top_gross_profit(data_frame=movies,colnames=['genres'])
    # A lot of movies had zero budget
    # I'll have to find a more robust formula for marginal roi
    # grouped_aggregated_genres_marginal = calculate_top_marginal_roi(movies=movies,colname='genres')
    # print(top_10_genres)
    # print(grouped_aggregated_genres_marginal)
    # no not for collective baragaing xD
    # there are 3 actor columns, so I union them into a single col
    actors_union = union_actor_columns(movies)
    top_10_actors_avg = calculate_top_gross_profit(data_frame=actors_union,colnames=['actor_name'],metric='mean')
    top_10_actors_total = calculate_top_gross_profit(data_frame=actors_union,colnames=['actor_name'])

    print(top_10_actors_avg)
    print(top_10_actors_total)

def main():
    print(test_df)

    full_run()
    


if __name__=='__main__':
    main()