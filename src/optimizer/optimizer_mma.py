import pulp
import pandas as pd
import numpy as np


class Optimizer:
    def __init__(self, df, sport, site, invert=False):
        self.df = df
        self.site = site
        self.sport = sport
        self.invert = invert

        self.rewards = []
        self.costs = []
        self.total_picks = []
        self.optimizer = pulp.LpProblem(self.sport, pulp.LpMaximize)
        self.lineup = []

        self.salaries = {}
        self.points = {}
        self.vars = {}
        
    def _set_vars(self):
        
        self.salaries = self.df[['Name', 'SAL']].set_index('Name').to_dict()['SAL']
        self.points = self.df[['Name', 'preds']].set_index('Name').to_dict()['preds']            

        self.vars = {k: pulp.LpVariable(k, cat="Binary") for k in self.salaries.keys()} 


    def solve(self):
        self._set_vars()
        
        for k, v in self.vars.items():
            self.costs += pulp.lpSum([self.salaries[k] * self.vars[k]])
            self.rewards += pulp.lpSum([self.points[k] * self.vars[k]])
            self.total_picks += pulp.lpSum([self.vars[k] * 1])

        self.optimizer += pulp.lpSum(self.rewards)
        self.optimizer += pulp.lpSum(self.total_picks) == 6
        
        if self.site == 'fd':
            self.optimizer += pulp.lpSum(self.costs) <= 100

        else:
            self.optimizer += pulp.lpSum(self.costs) <= 50000
        
        self.optimizer.solve()


    def get_lineup(self):
        for v in self.optimizer.variables():
            if v.varValue > 0:
                self.lineup.append(' '.join(v.name.split('_')))

