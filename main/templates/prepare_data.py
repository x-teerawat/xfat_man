from _libs import *

def prepare_data(df:pd.DataFrame):
    ### Prep data
    df_copy = df.copy()
    df_copy['timestamp'] = pd.to_datetime(df_copy.timestamp, unit="ms") # Convert timestamp
    ### Convert time zone
    est = pytz.timezone('US/Eastern')
    utc = pytz.utc
    df_copy['timestamp'] = [df_copy['timestamp'][i].replace(tzinfo=utc).astimezone(est) for i in range(len(df_copy))]
    df_copy['timestamp'] = [df_copy['timestamp'][i].replace(tzinfo=None) for i in range(len(df_copy))] # Remove timezone
    df_copy['date'] = [df_copy.timestamp[i].strftime("%Y-%m-%d") for i in range(len(df_copy))] # Date
    df_copy['time'] = [df_copy.timestamp[i].strftime("%H:%M:%S") for i in range(len(df_copy))] # Time
    df_copy['day'] = [df_copy.timestamp[i].strftime("%a") for i in range(len(df_copy))] # Day
    df_copy.index = df_copy.timestamp # Set index
    df_copy.index.name = None # Remove index name
    df_copy.drop(columns=['vwap', 'timestamp', 'transactions', 'otc'], inplace=True) # Drop timestamp column

    return df_copy
