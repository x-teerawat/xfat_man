import sys
sys.path.insert(0, 'main/templates')
from _backtesting import Backtesting
from _forward_testing import ForwardTesting

if __name__=="__main__":
    Backtesting(
        test_type="backtesting",
        stock_name="TQQQ",
        list_n_ema=[[12, 24]],
        list_n_time_frames=[15], # Unit: second
        initial_cash=100000,
        n_cut_loss=-0.3,
        list_buy_strategies=["bullish_divergence"], # ema_crossover, v_shape, turtle_shell, bullish_divergence
        list_sell_strategies=["bearish_divergence"], # ema_crossunder, inverse_v_shape, inverse_turtle_shell, bearish_divergence
        test_date = "2024-01-18",
        n_lags = 10,
        maker_fees = 0.002,
        taker_fees = 0.002,
        up_thresh = 0.001,
        down_thresh = -0.001,
        show_verbose=True,
        # show_plot=True,
        save_plot=True,
        # save_to_database=True,
    ).run_backtesting()
