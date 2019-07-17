import pandas as pd
import numpy as np

from optimizer import Optimizer

from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

opt = Optimizer()

class Model:
    
    def __init__(self):
        self.data = None
    
    def train(self):
        pass
    
    def test(self):
        pass        
        

class Performance:
    
    def __init__(self):
        pass
    
