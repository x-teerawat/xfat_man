class ForwardTesting():
    def __init__(
        self,
        test_type="forward_testing",
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

    def run_forward_testing(self):
        print("run_forward_testing")