from pga.model.build_model import Model
from sklearn.linear_model import BayesianRidge

def update_model(df, site):
    ridge = BayesianRidge()
    params = []
    
    model = Model(ridge, params, df)

    model.train()
    model.save(site)

if __name__ == '__main__':
    pass
