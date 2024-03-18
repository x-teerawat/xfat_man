from _libs import *

def prepare_data_for_database(self):
    buy_data = self.log_data[self.log_data.status=="buy"]
    buy_data = buy_data[["open"]]
    buy_data.reset_index(inplace=True)
    buy_data.columns = ["buyTime", "buyPrice"]
    buy_data['buyId'] = self.buy_id
    
    sell_data = self.log_data[self.log_data.status=="sell"]
    sell_data = sell_data[["open"]]
    sell_data.reset_index(inplace=True)
    sell_data.columns = ["sellTime", "sellPrice"]
    sell_data['sellId'] = self.sell_id

    buy_and_sell_data = pd.concat([buy_data, sell_data], axis=1)
    buy_and_sell_data["pnlUsd"] = (((buy_and_sell_data["sellPrice"]/buy_and_sell_data["buyPrice"])-1)+1) * self.initial_cash
    buy_and_sell_data["pnlPct"] = ((buy_and_sell_data["sellPrice"]/buy_and_sell_data["buyPrice"])-1) * 100
    buy_and_sell_data["algorithmId"] = self.algorithm_id
    buy_and_sell_data["strategyId"] = self.strategy_id
    buy_and_sell_data["testType"] = self.test_type

    self.lst_buy_and_sell_data = []
    for a_i, strategy_id, b_t, b_p, b_i, s_t, s_p, s_i, t_t in zip(
        buy_and_sell_data.algorithmId.values,
        buy_and_sell_data.strategyId.values,
        buy_and_sell_data.buyTime.values,
        buy_and_sell_data.buyPrice.values,
        buy_and_sell_data.buyId.values,
        buy_and_sell_data.sellTime.values,
        buy_and_sell_data.sellPrice.values,
        buy_and_sell_data.sellId.values,
        buy_and_sell_data.testType.values
    ):
        self.lst_buy_and_sell_data.append({"algorithmId": int(a_i), "strategyId": int(strategy_id), "buyTime": pd.to_datetime(b_t), "buyPirce": np.round(b_p, 2), "buyId": int(b_i), "sellTime": pd.to_datetime(s_t), "sellPirce": np.round(s_p, 2), "sellId": int(s_i), "testType": t_t})

    try:
        self.win_rate_pct = np.round(len(buy_and_sell_data[buy_and_sell_data.pnlPct > 0]) / len(buy_and_sell_data) * 100, 4)
    except: # division by zero
        self.win_rate_pct = 0

    self.total_pnl_pct = buy_and_sell_data.pnlPct.sum()
    
