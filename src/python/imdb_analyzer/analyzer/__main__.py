import argparse,os
from analyzer import *


def full_run():
    file_dir = os.path.split(os.path.abspath(__file__))[0]
    DEFAULT_DATA_PATH = os.path.abspath(file_dir+'/../../../../data/movie_metadata.csv')
    DESCRIPTION="""
    reads in imbd data file shaped like this:
    https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset/data

    Displays top 10 genres by average gross profit and top 10 actors by total gross profit (union of all 3 actor fields)

    --data-file allows you to provide your own data file when running the module as a script
    - File must be properly formatted using colnames from https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset/data
    - if not provided, will use test file https://github.com/HarryCaveMan/imdb_analysis/blob/main/data/movie_metadata.csv
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--data-file', type=str,default=DEFAULT_DATA_PATH,help='alternative data file (default is https://github.com/HarryCaveMan/imdb_analysis/blob/main/data/movie_metadata.csv')
    # parsing args in unit tests causes error, this workaround doesn't break the module scripting
    if __name__=="__main__":
        args = parser.parse_args()
        data_path = args.data_file
    else: data_path = DEFAULT_DATA_PATH
    # end workaround (got me +2% coverage adding tests for main script)
    movies = read_file(data_path)
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

full_run()