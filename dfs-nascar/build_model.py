import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from nascar_lineups.clean_data import LoadData
from nascar_lineups.model import Model


def pull_data():
    df = LoadData('tmp.ini', 'nascar_linestar')
    df.setup_connection()
    df.create_df()
    df.data_clean()
    
    X = df.df.drop(columns=['race_date', 'ps'])
    y = df.df['ps']

    return X, y


def build_model(X, y, path):

    raw_model = RandomForestRegressor()
    params = []
    
    model = Model(raw_model, params)
    model.train(X, y)
    
    model.save(path)


if __name__ == '__main__':
    X, y = pull_data()
    build_model(X, y, './nascar_model.pkl')
