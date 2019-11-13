from raw_data_pull.etl_sportsline import SportslineData
from raw_data_pull.etl_linestarapp import LinestarappData

def pull_data(sport, site):
    linestar = LinestarappData(sport, site)
    linestar.update_data()
    
    sportsline = SportslineData(sport)
    sportsline.update_articles()


if __name__ == '__main__':
    pass


