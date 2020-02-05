import pytest
from dfs.raw_data_pull.etl import LinestarappData

@pytest.fixture
def new_class():
    linestarapp_class = LinestarappData('nba', 'fd')

    return linestarapp_class

class TestLinestarappData:
    
    def test_get_pid(self, new_class):
        reg_key = 'nba/linestarapp/dk_1000.json'
        reg_expected = 1000
        reg_actual = new_class._get_pid(reg_key)

        proj_key = 'nascar/linestarapp/fd_274_projections.json'
        proj_expected = 274
        proj_actual = new_class._get_pid(proj_key)
        
        assert reg_expected == reg_actual, 'Regular pid incorrect.'
        assert proj_expected == proj_actual, 'Projected pid incorrect.'


    def test_delete_projections(self):
        pass
    
    
    def test_update_data(self):
        pass
    
    
    def test_get_max_pid(self):
        pass
    
    
    def test_pull_json_data(self):
        pass
    
    
    def test_check_projection(self):
        pass
    

    def test_log_file(self):
        pass
    




