from _libs import *
from _funcs import *

def get_data_for_backtesting(stock_name, train_date, test_date):
    # Get, Prep, and Clean data
    df = get_data(ticker=stock_name, unit="second", _from=train_date, to=test_date)
    prepared_data = prepare_data(df)
    cleaned_data = clean_data(prepared_data)

    test_data = prepared_data[(prepared_data.index>=pd.to_datetime(test_date))*(prepared_data.index<pd.to_datetime(test_date)+relativedelta(days=1)*(prepared_data.index>=pd.to_datetime(str(test_date) + " " + "09:30:00"))*(prepared_data.index<=pd.to_datetime(str(test_date) + " " + "15:59:59")))]
    test_data = test_data[["open", "high", "low", "close", "volume"]]
    train_data = cleaned_data[cleaned_data.index<test_data.index[0]]

    return train_data, test_data