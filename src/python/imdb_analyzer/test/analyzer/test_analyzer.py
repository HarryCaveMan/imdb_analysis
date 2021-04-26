import os,sys
import pandas as pd
file_dir = os.path.split(os.path.abspath(__file__))[0]
DATA_PATH = os.path.abspath(file_dir+'../../../../../../data/movie_metadata.csv')
# insert analyzer package root
sys.path.insert(0,os.path.abspath(file_dir+'../../../analyzer'))
from analyzer_core import *

#build small table I can hand calculate on to verify
TEST_COLUMN_NAMES = ['actor_1_name','actor_2_name','actor_3_name','genres','budget','gross']
TEST_COLUMNS = [
    ['Aaahnold','Lucille Ball','Aaahnold','Aaahnold','Vinnie Jones','Lucille Ball'],
    ['Lucille Ball','Aaahnold','Vinnie Jones','Lucille Ball','Aaahnold','Vinnie Jones'],
    # Just using a new actor (Mel Gibson) only on one row and setting this film's gross to zero
    # This gives gives me three easy tests for my math functions:
    # Aaahnold and Vinnie MUST have lower ranks than lucy, dragged down by Mel
    # Mel MUST be in last with zero gross
    # Lucy MUST be in first
    # having all other rows same just makes manual math easier on me for remaining tests
    ['Vinnie Jones','Vinnie Jones','Mel Gibson','Vinnie Jones','Lucille Ball','Aaahnold'],
    ['comedy','action','action','comedy','rom com','scifi'],
    [10,100,50,80,1000,0],
    # Set Mel gibsons row to zero gross
    [1000,10000,0,500,1500,10000]
]

TEST_DF = pd.DataFrame(
    dict(zip(TEST_COLUMN_NAMES,TEST_COLUMNS))
    ,index=range(6)
)

# just making sure everything works together as external library
def full_run():
    movies = read_file(DATA_PATH)
    top_10_genres_avg = calculate_top_gross_profit(data_frame=movies,colnames=['genres'],metric='mean')
    top_10_genres_total = calculate_top_gross_profit(data_frame=movies,colnames=['genres'])
    # A lot of movies had zero budget which caused infinity marginal roi
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
    movies = TEST_DF    
    top_genres_mean = calculate_top_gross_profit(data_frame=movies,colnames=['genres'],top_n=6,metric='mean')
    print('Top genres (metric average):')
    print(top_genres_mean)
    # I calculated these by hand to verify
    print('Verifying top grossing genre is scifi...')
    assert top_genres_mean.index[0] == 'scifi'
    print('Verifying Scifi Averages...')
    assert top_genres_mean.loc['scifi']['gross_profit'] == 10000
    assert top_genres_mean.loc['scifi']['gross'] == 10000
    assert top_genres_mean.loc['scifi']['budget'] == 0
    print('Scifi Averages Verified! Verifying Action Averages...')
    assert top_genres_mean.loc['action']['gross_profit'] == 4925
    assert top_genres_mean.loc['action']['gross'] == 5000
    assert top_genres_mean.loc['action']['budget'] == 75
    print('Scifi Averages Verified! Verifying Comedy Averages...')
    assert top_genres_mean.loc['comedy']['gross_profit'] == 705
    assert top_genres_mean.loc['comedy']['gross'] == 750
    assert top_genres_mean.loc['comedy']['budget'] == 45
    print('Scifi Averages Verified! Verifying Rom Com Averages...')
    assert top_genres_mean.loc['rom com']['gross_profit'] == 500
    assert top_genres_mean.loc['rom com']['gross'] == 1500
    assert top_genres_mean.loc['rom com']['budget'] == 1000
    print('All tests passed for Average metric!\n\n')
    print('Verifying actor union function...')
    actors_union = union_actor_columns(TEST_DF)
    assert list(actors_union['actor_name']) == list(TEST_DF['actor_1_name'])+list(TEST_DF['actor_2_name'])+list(TEST_DF['actor_3_name'])
    print('Function Verified!\n\n')
    print('Top Actors (metric sum):')
    top_actors_gross_sum = calculate_top_gross_profit(data_frame=actors_union,colnames=['actor_name'],top_n=6,metric='sum')
    print(top_actors_gross_sum)
    print('Verifying first Lucille Ball and last place Mel Gibson...')
    assert top_actors_gross_sum.index[0] == 'Lucille Ball'
    assert top_actors_gross_sum.index[3] == 'Mel Gibson'
    print('First and last Verified, verifying Lucille Ball stats...')
    assert top_actors_gross_sum.loc['Lucille Ball']['gross_profit'] == 21810
    assert top_actors_gross_sum.loc['Lucille Ball']['gross'] == 23000
    assert top_actors_gross_sum.loc['Lucille Ball']['budget'] == 1190
    print('Lucille Ball Verified, verifying Mel Gibson stats...')
    assert top_actors_gross_sum.loc['Mel Gibson']['gross_profit'] == -50
    assert top_actors_gross_sum.loc['Mel Gibson']['gross'] == 0
    assert top_actors_gross_sum.loc['Mel Gibson']['budget'] == 50
    print('Mel Gibson Verified, verifying Vinny Jones...')
    assert top_actors_gross_sum.loc['Vinnie Jones']['gross_profit'] == 21760
    assert top_actors_gross_sum.loc['Vinnie Jones']['gross'] == 23000
    assert top_actors_gross_sum.loc['Vinnie Jones']['budget'] == 1240
    print('Vinnie Jones Verified, verifying Vinny Jones...')
    assert top_actors_gross_sum.loc['Aaahnold']['gross_profit'] == 21760
    assert top_actors_gross_sum.loc['Aaahnold']['gross'] == 23000
    assert top_actors_gross_sum.loc['Aaahnold']['budget'] == 1240
    print('All tests passed!')
    # full_run()


def test_analyzer_suite():
    main()

if __name__=='__main__':
    main()