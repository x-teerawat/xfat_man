from _libs import *

def clean_data(prepared_data):
    unique_date = prepared_data.date.unique()
    lst_cleaned_data = []

    for _date in unique_date:
        prepared_data_copy = prepared_data[prepared_data.date==_date]

        ### Determine start and end trading time
        if prepared_data_copy.time[0] != "04:00:00": # Start trading time
            prepared_data_copy.loc[pd.to_datetime(prepared_data_copy.date[0] + " 04:00:00")] = np.nan
            prepared_data_copy.loc[pd.to_datetime(prepared_data_copy.date[0] + " 04:00:00"), 'date'] = prepared_data_copy.date[0]
            prepared_data_copy.loc[pd.to_datetime(prepared_data_copy.date[0] + " 04:00:00"), 'time'] = prepared_data_copy.time[0]
            prepared_data_copy.loc[pd.to_datetime(prepared_data_copy.date[0] + " 04:00:00"), 'day'] = prepared_data_copy.day[0]
        if prepared_data_copy.time[-1] != "19:59:59": # End trading time
            prepared_data_copy.loc[pd.to_datetime(prepared_data_copy.date[0] + " 19:59:59")] = np.nan
            prepared_data_copy.loc[pd.to_datetime(prepared_data_copy.date[0] + " 19:59:59"), 'date'] = prepared_data_copy.date[0]
            prepared_data_copy.loc[pd.to_datetime(prepared_data_copy.date[0] + " 19:59:59"), 'time'] = prepared_data_copy.time[0]
            prepared_data_copy.loc[pd.to_datetime(prepared_data_copy.date[0] + " 19:59:59"), 'day'] = prepared_data_copy.day[0]
        prepared_data_copy.sort_index(inplace=True)

        ### Search missing time
        prepared_data_copy['diff_time'] = prepared_data_copy.index.diff()
        prepared_data_copy['diff_second'] = [prepared_data_copy.diff_time[i].seconds for i in range(len(prepared_data_copy))]
        prepared_data_copy['n_missing_seconds'] = prepared_data_copy.diff_second-1
        prepared_data_copy.n_missing_seconds.fillna(0, inplace=True)
        ## Generate missing times
        lst_missing_time = [[prepared_data_copy.index[i-1]+relativedelta(seconds=n_missing_seconds) for n_missing_seconds in range(1, int(prepared_data_copy.n_missing_seconds[i])+1)] for i in range(len(prepared_data_copy)) if prepared_data_copy.n_missing_seconds[i] != 0]
        lst_missing_time = [
            missing_time
            for lst_in_lst_missing_time in lst_missing_time
            for missing_time in lst_in_lst_missing_time
        ] # Flat list in list
        prepared_data_missing_time = pd.DataFrame(index=lst_missing_time) # Convert list to dataframe

        ### Concat missing time with existing data
        prepared_data_copy = pd.concat([prepared_data_copy, prepared_data_missing_time], axis=0)
        prepared_data_copy.sort_index(inplace=True)
        prepared_data_copy

        ### Check
        n_missing_values = prepared_data_copy[(prepared_data_copy.index>=f"{_date} 09:30:00")*(prepared_data_copy.index<=f"{_date} 15:59:59")].open.isna().sum()
        n_data = len(prepared_data_copy[(prepared_data_copy.index>=f"{_date} 09:30:00")*(prepared_data_copy.index<=f"{_date} 15:59:59")])
        print(f"In {_date} from 09:30:00 to 15:59:59, There're missing values: {n_missing_values}/{n_data} ({np.round(n_missing_values/n_data*100, 4)}%)")

        ### Fill missing values with previous 14 days
        prepared_data_copy['open'] = prepared_data_copy.open.rolling(window=14, min_periods=1).mean()
        prepared_data_copy['high'] = prepared_data_copy.high.rolling(window=14, min_periods=1).mean()
        prepared_data_copy['low'] = prepared_data_copy.low.rolling(window=14, min_periods=1).mean()
        prepared_data_copy['close'] = prepared_data_copy.close.rolling(window=14, min_periods=1).mean()

        ### Determine open market
        prepared_data_copy = prepared_data_copy[(prepared_data_copy.index>=f"{_date} 09:30:00")*(prepared_data_copy.index<=f"{_date} 15:59:59")]

        ### Select preferred columns
        prepared_data_copy = prepared_data_copy[['open', 'high', 'low', 'close']]
        
        ### Append
        lst_cleaned_data.append(prepared_data_copy)

    ### Concat
    cleaned_data = pd.concat(lst_cleaned_data)

    return cleaned_data