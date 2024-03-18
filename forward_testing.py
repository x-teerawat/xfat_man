from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage
from polygon.websocket.models.common import Feed, Market
from typing import List
import pytz
import pandas as pd
import numpy as np

### To calculate time
from dateutil.relativedelta import relativedelta

from strategy_v_0_0 import Strategy

class ForwardTesting(Strategy):
    def __init__(
        self,
        n_fast_ema=12,
        n_slow_ema=24,
        list_n_time_frames=[15], # Unit: second
        initial_cash=100000,
        n_cut_loss=-0.3,
        buy_strategy = 1,
        sell_strategy = 3,
        test_date = "2024-01-18",
        up_thresh = 0.001,
        down_thresh = -0.001,
        verbose=False,
        show_plot=False,
        save_plot=False,
    ):
        self.n_fast_ema = n_fast_ema
        self.n_slow_ema = n_slow_ema
        self.list_n_time_frames = list_n_time_frames
        self.initial_cash = initial_cash
        self.n_cut_loss = n_cut_loss/100

        self.buy_strategy = buy_strategy
        self.sell_strategy = sell_strategy
        self.show_plot = show_plot
        self.save_plot = save_plot
        self.up_thresh = up_thresh
        self.down_thresh = down_thresh

        self.create_folder()

        self.ws = WebSocketClient(api_key="YIhBBbc2BuaZGiDd9Ax4PI5tLLIS3JJd", subscriptions=["A.TQQQ"])

        prepared_df = pd.read_pickle("prepared_df_1s_tqqq_2024-01-01_2024-02-01.pkl")
        cleaned_df = pd.read_pickle("cleaned_df_1s_tqqq_2024-01-01_2024-02-01.pkl")

        test_date = "2024-02-01"
        self.test_data = prepared_df[(prepared_df.index>=pd.to_datetime(test_date))*(prepared_df.index<pd.to_datetime(test_date)+relativedelta(days=1)*(prepared_df.index>=pd.to_datetime(str(test_date) + " " + "09:30:00"))*(prepared_df.index<=pd.to_datetime(str(test_date) + " " + "15:59:59")))]
        self.test_data = self.test_data[["open", "high", "low", "close", "volume"]]
        train_data = cleaned_df[cleaned_df.index<self.test_data.index[0]]
        
        ### All data
        try:
            self.existing_data = self.load('data/existing_data.pkl')
            self.all_new_data = self.load('data/all_new_data.pkl')
            self.nav_data = self.load('data/nav_data.pkl')

            self.existing_data_of_multi_time_frames = self.load('data/existing_data_of_multi_time_frames.pkl')
            self.convert_existing_data_to_multi_time_frames = self.load('data/convert_existing_data_to_multi_time_frames.pkl')
            self.all_new_data_of_multi_time_frames = self.load('data/all_new_data_of_multi_time_frames.pkl')
            self.zig_zag_data_of_multi_time_frames = self.load('data/zig_zag_data_of_multi_time_frames.pkl')

            self.cycle_nth = self.load('data/cycle_nth.pkl')
            self.round_nth = self.load('data/round_nth.pkl')
            self.update_interfece_nth = self.load('data/update_interfece_nth.pkl')
            self.round_nth_of_multi_time_frames = self.load('data/round_nth_of_multi_time_frames.pkl')

            self.log_data = self.load('data/log_data.pkl')

        except:
            self.existing_data = train_data.copy()
            self.all_new_data = pd.DataFrame()
            self.nav_data = pd.DataFrame()

            self.existing_data_of_multi_time_frames = [pd.DataFrame() for i in range(len(self.list_n_time_frames))] 
            self.convert_existing_data_to_multi_time_frames() # Convert existing data to multi time frames
            self.all_new_data_of_multi_time_frames = [pd.DataFrame() for i in range(len(self.list_n_time_frames))]
            self.zig_zag_data_of_multi_time_frames = [pd.DataFrame() for i in range(len(self.list_n_time_frames))]
            
            self.cycle_nth = 1 # To count the cycle
            self.round_nth = 0 # To select the cycle
            self.update_interfece_nth = 1 # To update the interface
            self.round_nth_of_multi_time_frames = [0 for i in range(len(self.list_n_time_frames))]

            self.log_data = pd.DataFrame()

    def handle_msg(self, msg: List[WebSocketMessage]):
        for m in msg:

            est = pytz.timezone('US/Eastern')
            utc = pytz.utc

            self.new_data = pd.DataFrame({
                'open': [m.open],
                'high': [m.high],
                'low': [m.low],
                'close': [m.close],
                'volume': [m.volume],
                'start_timestamp': [pd.to_datetime(m.start_timestamp, unit='ms')],
            })
            self.new_data['start_timestamp'] =  [self.new_data['start_timestamp'][i].replace(tzinfo=utc).astimezone(est) for i in range(len(self.new_data))]
            self.new_data['start_timestamp'] =  [self.new_data['start_timestamp'][i].replace(tzinfo=None) for i in range(len(self.new_data))] # Remove timezoneself.new_data.replace(tzinfo=None)
            self.new_data.set_index('start_timestamp', inplace=True)
            self.new_data.index.name = None

            self.run_strategy()

        self.save_data_when_disconnecting()

    def run_forward_test(self):
        self.ws.run(self.handle_msg)

if __name__ == "__main__":
    forward_testing = ForwardTesting(
                n_fast_ema=12,
                n_slow_ema=24,
                list_n_time_frames=[15], # Unit: second
                initial_cash=100000,
                n_cut_loss=-0.3,
                buy_strategy = 1,
                sell_strategy = 3,
                test_date = "2024-01-18",
                up_thresh = 0.001,
                down_thresh = -0.001,
                verbose=False,
                show_plot=False,
                save_plot=True,
            )
    while True:
        try:
            forward_testing.run_forward_testing()
        except:
            pass

