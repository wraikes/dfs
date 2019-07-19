import configparser
from sklearn.ensemble import RandomForestRegressor

from load_data import LoadData
from model import Model


def pull_data():
    cfg = configparser.ConfigParser()
    cfg.read('build_model.ini')
    
    label = eval(cfg['TABLEVARIABLES']['label'])
    predictors = eval(cfg['TABLEVARIABLES']['predictors'])
    non_numeric_cols = eval(cfg['TABLEVARIABLES']['non_numeric_cols'])

    df = LoadData('tmp.ini', 'nascar_linestar')
    df.setup_connection()
    df.create_df()
    df.data_clean(non_numeric_cols, predictors, label)
    
    X = df.df[predictors]
    y = df.df[label]

    return X, y


def build_model(X, y, path):

    raw_model = RandomForestRegressor()
    params = []
    
    model = Model(raw_model, params)
    model.train(X, y)
    
    model.save(path)


if __name__ == '__main__':
    X, y = pull_data()
    build_model(X, y, './nascar_model.joblib')
