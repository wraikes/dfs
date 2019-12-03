import pulp
import pandas as pd
import numpy as np


class Optimizer:
    def __init__(self, df, sport, site, invert=False):
        self.df = df
        self.site = site
        self.sport = sport
        self.invert = invert
        
        self.salaries = self.df[['name', 'salary']].set_index('name').to_dict()['salary']
        self.points = self.df[['name', 'preds']].set_index('name').to_dict()['preds']
        self.rewards = []
        self.costs = []
        self.total_picks = []
        self.optimizer = pulp.LpProblem(self.sport, pulp.LpMaximize)
        self.vars = {k: pulp.LpVariable(k, cat="Binary") for k in self.salaries.keys()} 
        self.lineup = []
        #self.teams #sport dependent (nba, nhl, etc.)

    def solve(self):
        for k, v in self.vars.items():
            self.costs += pulp.lpSum([self.salaries[k] * self.vars[k]])
            self.rewards += pulp.lpSum([self.points[k] * self.vars[k]])
            self.total_picks += pulp.lpSum([self.vars[k] * 1])

        #sport dependent
        self.optimizer += pulp.lpSum(self.rewards)
        if self.site == 'fd':
            self.optimizer += pulp.lpSum(self.costs) <= 60000
        else:
            self.optimizer += pulp.lpSum(self.costs) <= 50000
        self.optimizer += pulp.lpSum(self.total_picks) == 6

        self.optimizer.solve()


    def get_lineup(self):
        for v in self.optimizer.variables():
            if v.varValue > 0:
                self.lineup.append(' '.join(v.name.split('_')))
