import numpy as np
import pandas as pd

from dateutil.relativedelta import relativedelta

from strategy_v_0_1 import Strategy

class Backtesting(Strategy):
    def __init__(
        self,
        stock_name="TQQQ",
        n_fast_ema=12,
        n_slow_ema=24,
        list_n_time_frames=[15], # Unit: second
        initial_cash=100000,
        n_cut_loss=-0.3,
        buy_strategy = "tf_15s_hl", # tf_15s_hl
        sell_strategy = 3,
        train_date = "2024-02-05",
        test_date = "2024-02-06",
        up_thresh = 0.001,
        down_thresh = -0.001,
        show_verbose=False,
        show_plot=False,
        save_plot=False,
    ):
        self.stock_name = stock_name
        self.n_fast_ema = n_fast_ema
        self.n_slow_ema = n_slow_ema
        self.list_n_time_frames = list_n_time_frames
        self.initial_cash = initial_cash
        self.n_cut_loss = n_cut_loss/100
        self.buy_strategy = buy_strategy
        self.sell_strategy = sell_strategy
        self.train_date = train_date
        self.test_date = test_date
        self.up_thresh = up_thresh
        self.down_thresh = down_thresh
        self.show_verbose = show_verbose
        self.show_plot = show_plot
        self.save_plot = save_plot

        ### Create a folder
        self.create_folder()

        # prepared_df = pd.read_pickle("prepared_df_1s_tqqq_2023-12-01_2024-01-26.pkl")
        # cleaned_df = pd.read_pickle("cleaned_df_1s_tqqq_2023-12-01_2024-01-26.pkl")
        prepared_df = pd.read_pickle(f"prepared_df_1s_{self.stock_name}_{self.train_date}_{self.test_date}.pkl")
        cleaned_df = pd.read_pickle(f"cleaned_df_1s_{self.stock_name}_{self.train_date}_{self.test_date}.pkl")

        ### For backtesting
        self.test_data = prepared_df[(prepared_df.index>=pd.to_datetime(self.test_date))*(prepared_df.index<pd.to_datetime(self.test_date)+relativedelta(days=1)*(prepared_df.index>=pd.to_datetime(str(self.test_date) + " " + "09:30:00"))*(prepared_df.index<=pd.to_datetime(str(self.test_date) + " " + "15:59:59")))].copy()
        self.test_data = self.test_data[["open", "high", "low", "close", "volume"]]
        train_data = cleaned_df[cleaned_df.index<self.test_data.index[0]]

        ### For forward testing
        # train_data = cleaned_df.copy()
        
        ### All data
        try:
            self.existing_data = self.load(f'{self.file_name}/existing_data.pkl')
            self.all_new_data = self.load(f'{self.file_name}/all_new_data.pkl')
            self.nav_data = self.load(f'{self.file_name}/nav_data.pkl')

            self.existing_data_of_multi_time_frames = self.load(f'{self.file_name}/existing_data_of_multi_time_frames.pkl')
            self.convert_existing_data_to_multi_time_frames = self.load(f'{self.file_name}/convert_existing_data_to_multi_time_frames.pkl')
            self.all_new_data_of_multi_time_frames = self.load(f'{self.file_name}/all_new_data_of_multi_time_frames.pkl')
            self.zig_zag_data_of_multi_time_frames = self.load(f'{self.file_name}/zig_zag_data_of_multi_time_frames.pkl')

            self.cycle_nth = self.load(f'{self.file_name}/cycle_nth.pkl')
            self.round_nth = self.load(f'{self.file_name}/round_nth.pkl')
            self.update_interfece_nth = self.load(f'{self.file_name}/update_interfece_nth.pkl')
            self.round_nth_of_multi_time_frames = self.load(f'{self.file_name}/round_nth_of_multi_time_frames.pkl')

            self.log_data = self.load(f'{self.file_name}/log_data.pkl')

        except:
            self.existing_data = train_data.copy()
            self.all_new_data = pd.DataFrame()
            self.nav_data = pd.DataFrame()

            self.time_in_multi_time_frames = ["" for i in range(len(self.list_n_time_frames))] 
            self.existing_data_of_multi_time_frames = [pd.DataFrame() for i in range(len(self.list_n_time_frames))] 
            self.convert_existing_data_to_multi_time_frames() # Convert existing data to multi time frames
            self.all_new_data_of_multi_time_frames = [pd.DataFrame() for i in range(len(self.list_n_time_frames))]
            self.zig_zag_data_of_multi_time_frames = [pd.DataFrame() for i in range(len(self.list_n_time_frames))]
            
            self.cycle_nth = 1 # To count the cycle
            self.round_nth = 0 # To select the cycle
            self.update_interfece_nth = 1 # To update the interface
            self.round_nth_of_multi_time_frames = [0 for i in range(len(self.list_n_time_frames))]

            self.log_data = pd.DataFrame()

    def run_backtesting(self):
        # for i in range(len(self.test_data)):
        for i in range(15):
            self.new_data = self.test_data.iloc[i].to_frame().T
        
            self.run_strategy()
        
        # self.save_data_when_disconnecting()

if __name__ == "__main__":
    Backtesting(
        stock_name="TQQQ",
        n_fast_ema=12,
        n_slow_ema=24,
        list_n_time_frames=[15], # Unit: second
        initial_cash=100000,
        n_cut_loss=-0.3,
        buy_strategy = "sg_tf_hl", # sg_tf_hl
        sell_strategy = "sg_tf_lh_or_ema_crossunder", # sg_tf_lh, sg_tf_ema_crossunder, sg_tf_lh_or_ema_crossunder, sg_tf_ema_crossunder_and_lh
        train_date = "2024-01-17",
        test_date = "2024-01-18",
        up_thresh = 0.001,
        down_thresh = -0.001,
        show_verbose=True,
        show_plot=False,
        # save_plot=True,
    ).run_backtesting()

    ### For many days
    # lst_date = (pd.date_range(start='2024-01-24', end='2024-01-26')).strftime("%Y-%m-%d")
    # # lst_date = (pd.date_range(start='2024-01-05', end='2024-01-26')).strftime("%Y-%m-%d")
    # lst_sell_strategies = [i for i in range(1, 5)]

    # for date in lst_date:
    #     for sell_strategy in lst_sell_strategies:

    #         try:
    #             BackTest(
    #                 n_fast_ema=12,
    #                 n_slow_ema=24,
    #                 list_n_time_frames=[15], # Unit: second
    #                 initial_cash=100000,
    #                 n_cut_loss=-0.3,
    #                 buy_strategy = 1, # 1
    #                 sell_strategy = sell_strategy, # 1, 2, 3, 4
    #                 test_date = date,
    #                 up_thresh = 0.001,
    #                 down_thresh = -0.001,
    #                 verbose=False,
    #                 # show_plot=False,
    #                 # save_plot=True,
    #             ).run_back_test()
    #         except:
    #             pass
    #         print(f"date: {date}, sell_strategy: {sell_strategy}")


    ### For many stocks
    # # lst_stock_names = ["TQQQ", "SQQQ", "NVDA", "TSLA", "NFLX"]
    # lst_stock_names = ["NVDA"]
    # lst_sell_strategies = ["sg_tf_lh", "sg_tf_ema_crossunder", "sg_tf_lh_or_ema_crossunder", "sg_tf_ema_crossunder_and_lh"]
    # # lst_sell_strategies = ["sg_tf_lh"]

    # for stock_name in lst_stock_names:
    #     for sell_strategy in lst_sell_strategies:
    #         print(f"stock_name: {stock_name}, sell_strategy: {sell_strategy}")

    #         Backtesting(
    #             stock_name=stock_name,
    #             n_fast_ema=12,
    #             n_slow_ema=24,
    #             list_n_time_frames=[15], # Unit: second
    #             initial_cash=100000,
    #             n_cut_loss=-0.3,
    #             buy_strategy = "sg_tf_hl", # sg_tf_hl
    #             sell_strategy = sell_strategy, # sg_tf_lh, sg_tf_ema_crossunder, sg_tf_lh_or_ema_crossunder, sg_tf_ema_crossunder_and_lh
    #             train_date = "2024-02-05",
    #             test_date = "2024-02-06",
    #             up_thresh = 0.001,
    #             down_thresh = -0.001,
    #             show_verbose=True,
    #             show_plot=False,
    #             save_plot=True,
    #         ).run_backtesting()