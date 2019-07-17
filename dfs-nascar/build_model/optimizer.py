import pulp
import pandas as pd
import numpy as np


class Optimizer:
    
    def __init__(self, df):
        self.df = df
        
        self.salaries = {}
        self.points = {} 
        self.rewards = []
        self.costs = []
        self.optimizer = pulp.LpProblem('nascar', LpMaximize)

df = pd.read_csv('./tmp.csv')
df = df[df.race_date=='2018-05-19']

salaries = df[['_name', 'sal']].set_index('_name').to_dict()['sal']
points = df[['_name', 'pp']].set_index('_name').to_dict()['pp']
rewards = []
costs = []
total_drivers = []
prob = pulp.LpProblem('nascar', pulp.LpMaximize)      
variables = {k: pulp.LpVariable(k, cat="Binary") for k in salaries.keys()} 

for k, v in variables.items():
    costs += pulp.lpSum([salaries[k] * variables[k]])
    rewards += pulp.lpSum([points[k] * variables[k]])
    total_drivers += pulp.lpSum([variables[k] * 1])

prob += pulp.lpSum(rewards)
prob += pulp.lpSum(costs) <= 50000
prob += pulp.lpSum(total_drivers) <= 5
prob.solve()


for v in prob.variables():
    if v.varValue > 0:
        print(v.name, v.varValue)

