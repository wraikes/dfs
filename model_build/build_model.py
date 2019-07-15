import psycopg2
import pandas as pd, numpy as np
import boto3
from data_load import connect_db



#setup backtest
#setup integer programming optimizer (pulp)
#select best model based on backtested optimizer results