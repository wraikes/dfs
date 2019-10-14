from etl_sportsline import SportslineData
from etl_linestarapp import LinestarappData

def main(sport, site):
    linestar = LinestarappData(sport, site)
    linestar.update_data()
    
    sportsline = SportslineData(sport)
    sportsline.update_articles()


if __name__ == '__main__':
    main('nascar', 'fd')


