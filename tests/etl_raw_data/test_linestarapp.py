import pytest
import pandas as pd
from datetime import datetime

from dfs.etl_raw_data import linestarapp

line_data_pull = linestarapp.PullData('nascar')

class TestLinestarappPullData():

    def test_get_pid(self):
        test_key_1 = 'nascar/linestarapp/dk_219.json'    
        test_key_2 = 'pga/linestarapp/fd_244_projections.json'

        actual_1 = line_data_pull._get_pid(test_key_1)
        actual_2 = line_data_pull._get_pid(test_key_2)
        expected_1 = 219
        expected_2 = 244

        assert actual_1 == expected_1
        assert actual_2 == expected_2


    def test_get_strings_projection(self):
        current_date = datetime.now().strftime('%m-%d-%Y')
        projection = True
        site = 'dk'
        pid = 218
        
        actual = line_data_pull._get_strings(site, pid, projection)
        expected = (
            'nascar/linestarapp/dk_218_projections.json', 
            'dk_218_projections_{}'.format(current_date)
        )

        assert expected[0] == actual[0]
        assert expected[1] == actual[1]
