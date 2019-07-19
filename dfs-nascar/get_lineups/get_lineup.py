from joblib import load
from get_data.scrape_nascar_data import NascarDataPull
from get_model.optimizer import Optimizer

df = NascarDataPull(train=False, pid=258)
df.pull_json_data()
df.extract_owner_data()
df.extract_table_data()

df = df._final_data.copy()
df = pd.DataFrame.from_dict(
    {(i, j, k): df[i][j][k] for i in df.keys() for j in df[i].keys() for k in df[i][j][k].keys()},
    orient='index'
)


def data_clean(non_numeric_cols, predictors):
    df = df[predictors].dropna() 

    for col in df.columns:
        if col not in non_numeric_cols:
            df[col] = pd.to_numeric(df[col])

    df['_name'] = df['name']            
    df = pd.get_dummies(df, columns=['_name', 'restrictor_plate', 'surface'], drop_first=True)
    df['race_date'] = pd.to_datetime(df['race_date']).dt.date  

    return df

non_numeric_cols = ['race_date', 'name', 'restrictor_plate', 'surface']
predictors = [
    'name',
    'salary',
    'race_date',
    'pp',
    'races',
    'wins',
    'top_fives',
    'top_tens',
    'avg_finish',
    'laps_led_race',
    'fastest_laps_race',
    'avg_pass_diff',
    'quality_passes_race',
    'fppg',
    'practice_laps',
    'practice_best_lap_time',
    'practice_best_lap_speed',
    'qualifying_pos',
    'qualifying_best_lap_time',
    'qualifying_best_lap_speed',
    'laps',
    'miles',
    'surface',
    'restrictor_plate',
    'cautions_race',
    'races_3',
    'finished',
    'wins_3',
    'top_5s',
    'top_10s',
    'avg_place',
    'races_4',
    'finished_4',
    'wins_4',
    'top_5s_4',
    'top_10s_4',
    'avg_place_4'
]


df = data_clean(df, non_numeric_cols, predictors)

# load model
model = joblib.load(path)
model.predict(df.drop(columns='name'))

# get predictions
opt = Optimizer(df)
opt.solve()
opt.get_lineup()

print(opt.lineup)
