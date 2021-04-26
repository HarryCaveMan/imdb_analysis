import os,sys
file_dir = os.path.split(os.path.abspath(__file__))[0]
test_data_path = os.path.abspath(file_dir+'../../../../../../data/movie_metadata.csv')
# insert analyzer package root
sys.path.insert(0,os.path.abspath(file_dir+'../../../analyzer'))
from file_utils import FileHandler


TEST_FILE_ROWS = 5043
TEST_FILE_COLS = 28
TEST_FILE_COLNAMES = set({'color','director_name','num_critic_for_reviews','duration','director_facebook_likes','actor_3_facebook_likes','actor_2_name','actor_1_facebook_likes','gross','genres','actor_1_name','movie_title','num_voted_users','cast_total_facebook_likes','actor_3_name','facenumber_in_poster','plot_keywords','movie_imdb_link','num_user_for_reviews','language','country','content_rating','budget','title_year','actor_2_facebook_likes','imdb_score','aspect_ratio','movie_facebook_likes'})

def main():
    no_file:bool = False
    other_file_error:bool = False
    file:FileHandler = FileHandler(test_data_path)
    try:
        data_frame = file.get_data()
        dict_list = file.get_data(return_type = 'dictlist')
    except FileNotFoundError as e:
        no_file = True
    except Exception as e:
        other_file_error = True
    
    print("Ensuring test data file is in correct location...")
    
    assert not no_file    
    
    print("File found! Validating test data file is not malformed...")

    assert not other_file_error

    print("File validated! Reading as DictList and verifying shape...")
    
    assert len(dict_list) == TEST_FILE_ROWS
    assert len(dict_list[0].keys()) == TEST_FILE_COLS
    assert set(dict_list[0].keys()) == TEST_FILE_COLNAMES
    
    print("Dict list verified! Reading in as DataFrame and verifying shape...")
    
    assert data_frame.shape[0] == TEST_FILE_ROWS
    assert data_frame.shape[1] == TEST_FILE_COLS
    assert set(data_frame.columns) == TEST_FILE_COLNAMES
    
    print("Done! All file tests passed!")

def test_file_suite():
    main()

if __name__=='__main__':
    main()