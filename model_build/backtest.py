
backtest_perf = {}

for date in df['date'].sort_values().unique():
    
    train_df = df[df['date'] < date]
    test_df = df[df['date'] == date]

    X_train = train_df['predictors']
    y_train = train_df['label']
    
    #build model off of train.
    
    
    #predict model on test
    
    
    #calculate performance
    
    
    #save performance
    backtest_perf[date] = performance


