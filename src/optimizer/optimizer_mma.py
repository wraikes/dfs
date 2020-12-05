import pulp
import pandas as pd
import numpy as np


class Optimizer:
    def __init__(self, df, sport, site, invert=False):
        self.df = df
        self.df.GID = self.df.GID.astype('str')
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
        
        for gid in self.df.GID.unique():
            df_gid = self.df[self.df.GID==gid]
            salary = list(df_gid[["Name", "SAL"]].set_index("Name").to_dict().values())[0]
            point = list(df_gid[["Name", "preds"]].set_index("Name").to_dict().values())[0]
            self.salaries[gid] = salary
            self.points[gid] = point

        self.vars = {k: pulp.LpVariable.dict(k, v, cat="Binary") for k, v in self.points.items()} 


    def solve(self):
        self._set_vars()
        
        for k, v in self.vars.items():
            self.costs += pulp.lpSum([self.salaries[k][i] * self.vars[k][i] for i in v])
            self.rewards += pulp.lpSum([self.points[k][i] * self.vars[k][i] for i in v])
            self.total_picks += pulp.lpSum([self.vars[k][i] * 1 for i in v])
            self.optimizer += pulp.lpSum([self.vars[k][i] for i in v]) <= 1

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
                self.lineup.append(' '.join(v.name.split('_')[1:]))

