from _libs import *

def get_data(
    ticker = "TQQQ", # Asset name
    api_key = "7PZTsP8NHCZy0cEsWRlgFaSa2Q8zm8Zb", # API key
    n = 1, # Number of days/hours/minutes/seconds
    unit = "second", # Unit
    _from = "2024-01-10",
    to = "2024-01-10",
    limit = 50000
):
    client = RESTClient(api_key=api_key)

    # List Aggregates (Bars)
    aggs = []
    for a in client.list_aggs(ticker=ticker, multiplier=n, timespan=unit, from_=_from, to=to, limit=limit):
        aggs.append(a)

    df = pd.DataFrame(aggs)

    return df