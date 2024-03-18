from _libs import *
from _funcs import *
from _utils import Utils
from get_data_for_backtesting import get_data_for_backtesting 

class Backtesting(Utils):
    def __init__(
        self,
        test_type="backtesting",
        stock_name="TQQQ",
        market_name="nasdaq",
        list_n_ema=[[12 ,24]],
        list_n_time_frames=[15], # Unit: second
        initial_cash=100000,
        n_cut_loss=-0.3,
        list_buy_strategies = ["1"],
        list_sell_strategies = ["1"],
        test_date = "2024-01-18",
        n_lags = 60,
        maker_fees = 0.002,
        taker_fees = 0.002,
        up_thresh = 0.001,
        down_thresh = -0.001,
        show_verbose=False,
        show_plot=False,
        save_plot=False,
        save_to_database=False
    ):
        self.test_type = test_type
        self.stock_name = stock_name
        self.market_name = market_name
        self.list_n_ema = list_n_ema
        self.list_n_time_frames = list_n_time_frames
        self.initial_cash = initial_cash
        self.n_cut_loss = n_cut_loss/100
        self.list_buy_strategies = list_buy_strategies
        self.list_sell_strategies = list_sell_strategies
        self.test_date = test_date
        self.n_lags = n_lags
        self.train_date = (pd.to_datetime(self.test_date) - relativedelta(days=1)).strftime("%Y-%m-%d")
        self.maker_fees = maker_fees # usd per share
        self.taker_fees = taker_fees # usd per share
        self.up_thresh = up_thresh
        self.down_thresh = down_thresh
        self.show_verbose = show_verbose
        self.show_plot = show_plot
        self.save_plot = save_plot
        self.save_to_database = save_to_database

        ### Create a folder
        create_folder(self)

        ### Default data and values
        # self.train_data, self.test_data = get_data_for_backtesting(self.stock_name, self.train_date, self.test_date)
        # prepared_data = pd.read_pickle("prepared_df_1s_TQQQ_2024-01-17_2024-01-18.pkl")
        # cleaned_data = pd.read_pickle("cleaned_df_1s_TQQQ_2024-01-17_2024-01-18.pkl")
        prepared_data = pd.read_pickle("C:\\Users\\TGAdmin\\Documents\\GitHub\\xmanhattan\\data\\prepared_df_1s_TQQQ_2024-01-17_2024-01-18.pkl")
        cleaned_data = pd.read_pickle("C:\\Users\\TGAdmin\\Documents\\GitHub\\xmanhattan\\data\\cleaned_df_1s_TQQQ_2024-01-17_2024-01-18.pkl")
        self.test_data = prepared_data[(prepared_data.index>=pd.to_datetime(test_date))*(prepared_data.index<pd.to_datetime(test_date)+relativedelta(days=1)*(prepared_data.index>=pd.to_datetime(str(test_date) + " " + "09:30:00"))*(prepared_data.index<=pd.to_datetime(str(test_date) + " " + "15:59:59")))]
        self.test_data = self.test_data[["open", "high", "low", "close", "volume"]]
        self.train_data = cleaned_data[cleaned_data.index<self.test_data.index[0]]

        self.existing_data = self.train_data.copy()
        self.all_new_data = pd.DataFrame()
        self.nav_data = pd.DataFrame()

        self.time_in_multi_time_frames = ["" for i in range(len(self.list_n_time_frames))] 
        self.existing_data_of_multi_time_frames = [pd.DataFrame() for i in range(len(self.list_n_time_frames))] 
        convert_existing_data_to_multi_time_frames(self)

        self.all_new_data_of_multi_time_frames = [pd.DataFrame() for i in range(len(self.list_n_time_frames))]
        self.zig_zag_data_of_multi_time_frames = [pd.DataFrame() for i in range(len(self.list_n_time_frames))]
        
        self.cycle_nth = 1 # To count the cycle
        self.round_nth = 0 # To select the cycle
        self.update_interfece_nth = 1 # To update the interface
        self.round_nth_of_multi_time_frames = [0 for i in range(len(self.list_n_time_frames))]

        self.log_data = pd.DataFrame()

    def run_backtesting(self):
        self.StartCountOfVShape, self.CountCandleOfVShape = 0, 0 # To compute "V shape"
        self.StartCountOfInverseVShape, self.CountCandleOfInverseVShape = 0, 0 # To compute "inverse  shape"

        # for self.i in range(len(self.test_data)):
        # for self.i in range(10000+1):
        for self.i in range(1999+1):
            # print(f"i: {self.i}")
            self.new_data = self.test_data.iloc[self.i].to_frame().T

            self.run_strategy()
        print("Backteting completed.")

        if self.save_to_database:
            convert_result_to_database(self)
            print("Convert result to database completed.")