from sklearn.linear_model import BayesianRidge
from prep_data import prep_data
from build_model import Model

def main():
    ridge = BayesianRidge()
    params = []
    
    df = prep_data()
    model = Model(ridge, params)
    
    model.train(df.drop(columns=['ps']), df['ps'])
    
    #save model
    model.save()


if __name__ == '__main__':
    main()
