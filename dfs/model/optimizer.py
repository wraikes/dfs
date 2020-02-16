import pulp
import pandas as pd
import numpy as np


class Optimizer:
    def __init__(self, df, site, invert=False):
        self.df = df
        self.site = site
        self.invert = invert
        
        self.rewards = []
        self.costs = []
        self.total_picks = []
        self.optimizer = pulp.LpProblem('optimizer', pulp.LpMaximize)
        self.lineup = []

        self.salaries = {}
        self.points = {}
        self.vars = {}
        




class OptimizerNascar(Optimizer):
    def __init__(self, df, site, invert=False):
        Optimizer.__init__(self, df, site, invert)    
        self.salary_constraint = 50000
        self.lineup_constraint = 6 if self.site == 'dk' else 5
        
    def _set_vars(self):
        self.salaries = self.df[['name', 'sal']].set_index('name').to_dict()['sal']
        self.points = self.df[['name', 'preds']].set_index('name').to_dict()['preds']            

        self.vars = {k: pulp.LpVariable(k, cat="Binary") for k in self.salaries.keys()}  
        
    def _set_optimizer(self):
        for k, v in self.vars.items():
            self.costs += pulp.lpSum([self.salaries[k] * self.vars[k]])
            self.rewards += pulp.lpSum([self.points[k] * self.vars[k]])
            self.total_picks += pulp.lpSum([self.vars[k] * 1])  

        self.optimizer += pulp.lpSum(self.rewards)
        self.optimizer += pulp.lpSum(self.total_picks) == self.lineup_constraint
        self.optimizer += pulp.lpSum(self.costs) <= self.salary_constraint            


    def get_lineup(self):
        self._set_vars()
        self._set_optimizer()
        self.optimizer.solve()

        for v in self.optimizer.variables():
            if v.varValue > 0:
                self.lineup.append(' '.join(v.name.split('_')))  
    
            
class OptimizerPGA(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)    
        self.salary_constraint = 60000 if self.site == 'fd' else 50000

    def _set_optimizer(self):
        for k, v in self.vars.items():
            self.costs += pulp.lpSum([self.salaries[k] * self.vars[k]])
            self.rewards += pulp.lpSum([self.points[k] * self.vars[k]])
            self.total_picks += pulp.lpSum([self.vars[k] * 1])

        self.optimizer += pulp.lpSum(self.rewards)
        self.optimizer += pulp.lpSum(self.total_picks) == 6
        self.optimizer += pulp.lpSum(self.costs) <= self.salary_constraint

  
                
class OptimizerNBA(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)
        self.salary_constraint = 56500 if self.site == 'fd' else 50000
    
    def _set_vars(self):
        for pos in self.df.pos.unique():
            df_pos = self.df[self.df.pos == pos]
            salary = list(df_pos[["name", "sal"]].set_index("name").to_dict().values())[0]
            point = list(df_pos[["name", "preds"]].set_index("name").to_dict().values())[0]
            self.salaries[pos] = salary
            self.points[pos] = point

        if self.site == 'fd':
            self.pos_num_available = {
                "PG": 2,
                "C": 1,
                "PF": 2,
                "SF": 2,
                "SG": 2
            }
            
        self.vars = {k: pulp.LpVariable.dict(k, v, cat="Binary") for k, v in self.points.items()}
                
    def _set_optimizer(self):
        self._set_vars()
        
        for k, v in self.vars.items():
            self.costs += pulp.lpSum([self.salaries[k][i] * self.vars[k][i] for i in v])
            self.rewards += pulp.lpSum([self.points[k][i] * self.vars[k][i] for i in v])
            self.total_picks += pulp.lpSum([1*self.vars[k][i] for i in v])
            self.optimizer += pulp.lpSum([self.vars[k][i] for i in v]) <= self.pos_num_available[k]

        self.optimizer += pulp.lpSum(self.rewards)
        self.optimizer += pulp.lpSum(self.total_picks) == 8
        self.optimizer += pulp.lpSum(self.costs) <= self.salary_constraint
