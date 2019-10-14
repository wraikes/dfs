import pulp
import pandas as pd
import numpy as np


class Optimizer:
    def __init__(self, df):
        self.df = df
        
        self.salaries = self.df[['name', 'salary']].set_index('name').to_dict()['salary']
        self.points = self.df[['name', 'preds']].set_index('name').to_dict()['preds']
        self.rewards = []
        self.costs = []
        self.total_drivers = []
        self.optimizer = pulp.LpProblem('nascar', pulp.LpMaximize)
        self.vars = {k: pulp.LpVariable(k, cat="Binary") for k in self.salaries.keys()} 
        self.lineup = []


    def solve(self):
        for k, v in self.vars.items():
            self.costs += pulp.lpSum([self.salaries[k] * self.vars[k]])
            self.rewards += pulp.lpSum([self.points[k] * self.vars[k]])
            self.total_drivers += pulp.lpSum([self.vars[k] * 1])

        self.optimizer += pulp.lpSum(self.rewards)
        self.optimizer += pulp.lpSum(self.costs) <= 50000
        self.optimizer += pulp.lpSum(self.total_drivers) <= 5
        self.optimizer.solve()


    def get_lineup(self):
        for v in self.optimizer.variables():
            if v.varValue > 0:
                self.lineup.append(' '.join(v.name.split('_')))
