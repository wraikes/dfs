import pytest
import pandas as pd

from dfs.etl_raw_data import linestarapp


line_data_pull = linestarapp.PullData('nascar')

def test_get_pid():
    test_key_1 = 'nascar/linestarapp/dk_219.json'    
    test_key_2 = 'pga/linestarapp/fd_244_projections.json'

    result_1 = line_data_pull._get_pid(test_key_1)
    result_2 = line_data_pull._get_pid(test_key_2)

    assert result_1 == 219
    assert result_2 == 244

def test_get_strings():
    pass

def test_check_projection():
    pass

def test_get_max_pid():
    pass

def test_delete_projections():
    pass

def update_data():
    #have to break this down into simpler functions (maybe)
    pass



