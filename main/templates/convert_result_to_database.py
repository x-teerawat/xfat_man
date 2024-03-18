from _libs  import *
from _funcs import *

def convert_result_to_database(self):
    ### Connect to MongoDB
    mongo_client = pymongo.MongoClient("mongodb://ubuntu:ubuntu@172.17.100.47:27017/")
    
    ### Check xmanhattan in MongoDB
    list_database_names =  mongo_client.list_database_names()
    n_xmanhattan_database =sum([i.startswith("xmanhattan_") for i in list_database_names])

    ### Determine buy, sell, and strategy
    buy_strategies = ("_or_").join(self.list_buy_strategies)
    sell_strategies = ("_or_").join(self.list_sell_strategies)
    strategy_descriptions = f"buy_strategies_{buy_strategies}__sell_strategies_{sell_strategies}"

    if n_xmanhattan_database == 0:
        ### Insert values to collection
        self.algorithm_id = 0
        stock_id = 0
        self.strategy_id = 0
        self.buy_id = 0
        self.sell_id = 0

    else:
        list_xmanhattan = [i for i in list_database_names if i.startswith("xmanhattan_")]
        self.algorithm_id = sorted([int(xmanhattan_nth.split("_")[1]) for xmanhattan_nth in list_xmanhattan])[-1] + 1

        ### Stock
        for xmanhattan_nth in list_xmanhattan:
            dict_stocks_in_database = {i['id']: i['stockName'] for i in mongo_client[xmanhattan_nth].stockDetails.find()}
            lst_stock_id = [k for k, stock_names_in_database in dict_stocks_in_database.items() if stock_names_in_database==self.stock_name]
            if len(lst_stock_id) == 0:
                stock_id = list(dict_stocks_in_database.keys())[-1] + 1
            else:
                stock_id = lst_stock_id[0]

        ### Buy
        dict_buy_strategies_in_database = {i['id']: i['buyStr'] for i in mongo_client[xmanhattan_nth].buyDetails.find() for xmanhattan_nth in list_xmanhattan}
        lst_buy_id = [k for k, strategy_name_in_database in dict_buy_strategies_in_database.items() if strategy_name_in_database==buy_strategies]
        if len(lst_buy_id) == 0:
            self.buy_id = list(dict_buy_strategies_in_database.keys())[-1] + 1
        else:
            self.buy_id = lst_buy_id[0]

        ### Sell
        dict_sell_strategies_in_database = {i['id']: i['sellStr'] for i in mongo_client[xmanhattan_nth].sellDetails.find() for xmanhattan_nth in list_xmanhattan}
        lst_sell_id = [k for k, strategy_name_in_database in dict_sell_strategies_in_database.items() if strategy_name_in_database==sell_strategies]
        if len(lst_sell_id) == 0:
            self.sell_id = list(dict_sell_strategies_in_database.keys())[-1] + 1
        else:
            self.sell_id = lst_sell_id[0]

        ### Strategy
        dict_strategy_details_in_database = {i['id']: i['strategyDesc'] for i in mongo_client[xmanhattan_nth].strategyDetails.find() for xmanhattan_nth in list_xmanhattan}
        lst_strategy_id = [k for k, strategy_description_in_database in dict_strategy_details_in_database.items() if strategy_description_in_database==strategy_descriptions]
        if len(lst_strategy_id) == 0:
            self.strategy_id = list(dict_strategy_details_in_database.keys())[0] + 1
        else:
            self.strategy_id = lst_strategy_id[0]

    ### Prepare data for database
    prepare_data_for_database(self)

    ### Create a collection
    db = mongo_client[f"xmanhattan_{self.algorithm_id}"]
    algorithmDetails = db["algorithmDetails"]
    stockDetails = db["stockDetails"]
    buyDetails = db["buyDetails"]
    sellDetails = db["sellDetails"]
    strategyDetails = db["strategyDetails"]
    backTesting = db["backTesting"]
    reports = db["reports"]

    algorithmDetails.insert_one({"id": self.algorithm_id, "algorithmDesc": f"list_n_ema_{self.list_n_ema}__list_n_time_frames_{self.list_n_time_frames}__n_cut_loss_{self.n_cut_loss}__test_date_{self.test_date}__up_thresh_{self.up_thresh}__down_thresh_{self.down_thresh}", "stock_id": stock_id, "self.strategy_id": self.strategy_id})
    stockDetails.insert_one({"id": stock_id, "stockName": self.stock_name, "marketName": self.market_name})
    buyDetails.insert_one({"id": self.buy_id, "buyStr": buy_strategies})
    sellDetails.insert_one({"id": self.sell_id, "sellStr": sell_strategies})
    strategyDetails.insert_one({"id": self.strategy_id, "strategyDesc": strategy_descriptions})
    backTesting.insert_many(self.lst_buy_and_sell_data)
    # try:
    #     backTesting.insert_many(self.lst_buy_and_sell_data)
    # except: ### There's no buy and sell data
    #     pass
    reports.insert_one({"winRatePct": self.win_rate_pct, "totalPnlPct": self.total_pnl_pct})