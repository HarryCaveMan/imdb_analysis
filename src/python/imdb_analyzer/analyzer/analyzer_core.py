import pandas as pd
import os

def read_file(filename:str,return_type:str='dataframe'):
    from .file_utils import FileHandler
    file:FileHandler = FileHandler(filename)
    return file.get_data(return_type=return_type)    

# def calculate_top_marginal_roi(data_frame,colname:str,top_n:int=10):
#     lookup_cols = ['gross','budget']
#     lookup_cols.extend(colnames)
#     missing_cols = set(lookup_cols).intersection(set(data_frame.columns)).difference(lookup_cols)
#     if(missing_cols != {}):
#         raise Error(f"Required columns {' '.join(missing_cols)} not in input data")
#     sub_frame = movies[lookup_cols].groupby(colnames).sum()
#     sub_frame['marginal_roi'] = (sub_frame['gross'] - sub_frame['budget'])/sub_frame['budget']
#     return sub_frame.nlargest(top_n,'marginal_roi')

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