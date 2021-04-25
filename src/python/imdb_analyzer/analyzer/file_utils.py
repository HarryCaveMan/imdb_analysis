import numpy as numpy
import pandas as pd


class FileHandler(object):
    valid_return_types=['dataframe','dictlist']
    def __init__(self,filename:str) -> None:
        self.filename:str = filename

    def _read_as_dataframe(self,index_col=None,header_row=0,sep:chr=',') -> pd.DataFrame:
        data:pd.DataFrame = pd.read_csv(self.filename,index_col=index_col,sep=sep,header=header_row)
        if 'Unnamed' in str(data.columns[-1]):
            data.drop(data.columns[-1], axis=1, inplace=True)
        return data

    # normally I'd try to create a fancy serializable class that uses less heap space than dict
    def _read_as_dictlist(self,header_row:int=0,sep:chr=',') -> list:
        with open(self.filename) as data_file:
            lines = data_file.readlines()
        colnames = lines.pop(header_row).split(',')
        if(colnames[-1]=='\n'):
            colnames = colnames[:-1]
            row_dicts:list = [
                dict(zip(colnames,line.split(sep)[:-1]))
                for line in lines
            ]
        else:
            row_dicts:list = [
                dict(zip(colnames,line.split(sep)))
                for line in lines
            ]
        return row_dicts

    def get_data(self,index_col=None,header_row=0,sep:chr=',',return_type='dataframe'):
        if return_type not in FileHandler.valid_return_types:
            raise Error("Unsupported return type! Valid types are 'dictlist' | 'dataframe'")
        if(return_type=='dictlist'):
            if index_col:
                raise Error("Index col not yet supported for dictlist")
            return self._read_as_dictlist(header_row=header_row,sep=sep)
        elif(return_type=='dataframe'):
            return self._read_as_dataframe(index_col=index_col,header_row=header_row,sep=sep)       