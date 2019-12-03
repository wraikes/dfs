from model.build_model import Model
from sklearn.linear_model import BayesianRidge

def update_model(df, sport, site):
    #need to configure this per sport (config file most likely)
    ridge = BayesianRidge()
    params = []
    
    model = Model(ridge, params, df)

    model.train()
    model.save(sport, site)

if __name__ == '__main__':
    pass
