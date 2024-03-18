import numpy as np
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt

### Data API
from polygon import RESTClient

### Disable warning
import warnings
warnings.filterwarnings("ignore")

### To calculate time
from dateutil.relativedelta import relativedelta

### To convert time zone
import pytz

### To convert the slope to the degree
import math

### Cadlestick plot
import mplfinance as mpf

### To save
import pickle

### To access a folder
import os


class Strategy():
    def __init__(
        self,
    ):
        some_strategy
        # pass

    ### Save data
    def save(self, folder_name, obj):
        with open(folder_name, 'wb') as fobj:
            pickle.dump(obj, fobj)

    ### Load data
    def load(self, folder_name):
        with open(folder_name, 'rb') as fobj:
            return pickle.load(fobj)

    ### Create a folder
    def create_folder(self):
        if self.save_plot:
            try:
                self.folder_name = f"plot__stock_name_{self.stock_name}__buy_strategy_{self.buy_strategy}__sell_strategy_{self.sell_strategy}__test_date_{self.test_date}__up_thresh_{self.up_thresh}__down_thresh_{self.down_thresh}"
                os.mkdir(self.folder_name)
            except:
                pass

    ### Save data when disconnecting
    def save_data_when_disconnecting(self):
        self.save(f'{self.folder_name}/existing_data.pkl', self.existing_data)
        self.save(f'{self.folder_name}/all_new_data.pkl', self.all_new_data)
        self.save(f'{self.folder_name}/nav_data.pkl', self.nav_data)

        self.save(f'{self.folder_name}/existing_data_of_multi_time_frames.pkl', self.existing_data_of_multi_time_frames)
        self.save(f'{self.folder_name}/convert_existing_data_to_multi_time_frames.pkl', self.convert_existing_data_to_multi_time_frames)
        self.save(f'{self.folder_name}/all_new_data_of_multi_time_frames.pkl', self.all_new_data_of_multi_time_frames)
        self.save(f'{self.folder_name}/zig_zag_data_of_multi_time_frames.pkl', self.zig_zag_data_of_multi_time_frames)

        self.save(f'{self.folder_name}/cycle_nth.pkl', self.cycle_nth)
        self.save(f'{self.folder_name}/round_nth.pkl', self.round_nth)
        self.save(f'{self.folder_name}/update_interfece_nth.pkl', self.update_interfece_nth)
        self.save(f'{self.folder_name}/round_nth_of_multi_time_frames.pkl', self.round_nth_of_multi_time_frames)

        self.save(f'{self.folder_name}/log_data.pkl', self.log_data)

    def search_update_position(
        self,
        n_time_frames
    ):
        return np.argwhere(n_time_frames==np.array(self.list_n_time_frames))[0][0]

    ### Convert to multi time frames data
    def convert_existing_data_to_multi_time_frames(
        self
    ):
        ### Convert to other time frame data
        for n_time_frames in self.list_n_time_frames:
            arr_idx = self.existing_data.index[::n_time_frames].values
            arr_open = self.existing_data.open.iloc[::n_time_frames].values
            arr_high = self.existing_data.groupby(np.arange(len(self.existing_data))//n_time_frames).high.max().values
            arr_low = self.existing_data.groupby(np.arange(len(self.existing_data))//n_time_frames).low.min().values
            arr_close = self.existing_data.close.iloc[n_time_frames-1::n_time_frames].values

            selected_position_nth = self.search_update_position(n_time_frames)
            converted_existing_data_multi_time_frames = pd.DataFrame({
                'open': arr_open,
                'high': arr_high,
                'low': arr_low,
                'close': arr_close
            }, index=arr_idx)
             
            self.existing_data_of_multi_time_frames[selected_position_nth] = converted_existing_data_multi_time_frames
    
    ### Plot
    def plot(self):
        ### Colors
        g_03 = "#A2D9CE"
        g_06 = "#16A085"
        g_10 = "#0B5345"

        r_03 = "#F5B7B1"
        r_06 = "#E74C3C"
        r_10 = "#78281F"

        b_03 = "#AED6F1"
        b_06 = "#3498DB"
        orange_06 = "#F39C12"

        ### Setup
        n_above_percentage = 0.5 # Unit: percentage
        n_below_percentage = 0.5 # Unit: percentage
        below_percentage = 1-(n_above_percentage/100)
        above_percentage = 1+(n_below_percentage/100)
        below_above_percentage = above_percentage*(1-0.0025)
        above_below_percentage = below_percentage*(1+0.0025)

        mc = mpf.make_marketcolors(
            up='green', 
            down='red', 
            edge='black', 
            volume='gray'
        )

        s = mpf.make_mpf_style(
            marketcolors=mc,
            gridcolor='lightgray',
            gridstyle=':',
            # facecolor='#a9a9a9',
            # figcolor='#a9a9a9',
            y_on_right=False
        )

        fig = mpf.figure(style=s, figsize=(7, 4))

        ax1 = fig.add_subplot(6, 1, (1, 4), style=s)
        ax2 = fig.add_subplot(6, 1, (5, 6), style=s, sharex=ax1)
        # ax3 = fig.add_subplot(8, 1, (7, 8), style=s, sharex=ax1)
        ax1.tick_params(labelbottom=False)
        # ax2.tick_params(labelbottom=False)

        plots = [
            ### ax1
            mpf.make_addplot(self.selected_zig_zag_data['pivot_price'], ax=ax1, color='purple', width=1),
            mpf.make_addplot(self.selected_zig_zag_data['pivot_ll']*below_percentage, scatter=True, marker="$LL$", markersize=150, ax=ax1, color=g_06),
            mpf.make_addplot(self.selected_zig_zag_data['pivot_hl']*below_percentage, scatter=True, marker="$HL$", markersize=150, ax=ax1, color=g_06),
            mpf.make_addplot(self.selected_zig_zag_data['pivot_hh']*above_percentage, scatter=True, marker="$HH$", markersize=150, ax=ax1, color=r_06),
            mpf.make_addplot(self.selected_zig_zag_data['pivot_lh']*above_percentage, scatter=True, marker="$LH$", markersize=150, ax=ax1, color=r_06),
            mpf.make_addplot(self.selected_zig_zag_data['pivot_buy_signal']*above_below_percentage, type="scatter", marker="^", markersize=150, ax=ax1, color=g_06),
            mpf.make_addplot(self.selected_zig_zag_data['pivot_sell_signal']*below_above_percentage, type="scatter", marker="v", markersize=150, ax=ax1, color=r_06),
            # mpf.make_addplot(self.log_data['pivots_cut_loss_at_the_same_time'], type="scatter", marker="v", markersize=200, ax=ax1, color=orange_06),
            # mpf.make_addplot(self.log_data['pivots_cut_loss_at_the_other_time'], type="scatter", marker="v", markersize=200, ax=ax1, color=orange_06),

            ### ax2
            mpf.make_addplot(self.selected_all_new_data[f'ema_{self.n_fast_ema}'], ax=ax2, color='red', width=1),
            mpf.make_addplot(self.selected_all_new_data[f'ema_{self.n_slow_ema}'], ylabel=f"EMA{self.n_fast_ema} (R) & EMA{self.n_slow_ema} (B)", ax=ax2, color='blue', width=1),

            ### ax3
            # mpf.make_addplot(self.selected_all_new_data['nav'], ax=ax3, color=b_03, width=1),
        ]

        ### To determine y lim
        ymin = self.selected_all_new_data['low'].min()*below_percentage*(1-0.003)
        ymax = self.selected_all_new_data['high'].max()*above_percentage*(1+0.003)

        chart_setup = dict(type='candle', ax=ax1, volume=False)

        mpf.plot(
            self.selected_all_new_data,
            **chart_setup,
            style=s,
            addplot=plots,
            xrotation=7,
            # tight_layout=True,
            tight_layout=False,
            # datetime_format="%d-%b-%y %H:%M:%S",
            datetime_format="%H:%M:%S",
            returnfig=True,
            ylim=(ymin, ymax)
        )
        
        ### EMA cutting down
        list_date_id_of_ema_cutting_down = self.selected_all_new_data[self.selected_all_new_data.IsEMACuttingDown==1].date_id.values
        if len(list_date_id_of_ema_cutting_down) >= 1:
            for ax in [ax1, ax2]:
                for x in list_date_id_of_ema_cutting_down:
                    ax.axvline(x=x, linestyle='--', color=r_06, alpha=0.75)

        if self.show_plot:
            ### Adjustments to plot
            plt.subplots_adjust(hspace=0)
            mpf.show()
            # plt.show(block=False)

        ### Save plot
        if self.save_plot:
            plt.draw()
            plt.savefig(f'{self.folder_name}/{self.round_nth}.png')
            plt.close()

    def convert_new_data_to_multi_time_frames(
        self
    ):
        ### Convert 1s time frame to other time frame data
        data_to_convert_time_frame = self.all_new_data.iloc[-self.n_time_frames:, :]

        idx = data_to_convert_time_frame.index[0]
        open_value = data_to_convert_time_frame.open[0]
        high_value = data_to_convert_time_frame.high.max()
        low_value = data_to_convert_time_frame.low.min()
        close_value = data_to_convert_time_frame.close[-1]

        self.converted_new_data_of_multi_time_frames = pd.DataFrame({
            'open': open_value,
            'high': high_value,
            'low': low_value,
            'close': close_value,
            'date_id': self.round_nth_of_multi_time_frames[self.selected_position_nth]
        }, index=[idx])

        ### Update
        self.all_new_data_of_multi_time_frames[self.selected_position_nth] = pd.concat([self.all_new_data_of_multi_time_frames[self.selected_position_nth], self.converted_new_data_of_multi_time_frames])

    def update_existing_data_of_multi_time_frames(
        self
    ):
        self.existing_data_of_multi_time_frames[self.selected_position_nth] = pd.concat([self.existing_data_of_multi_time_frames[self.selected_position_nth], self.converted_new_data_of_multi_time_frames])

    ### For zig zag pattern
    def _identify_initial_pivot(
        self,
        X,
        up_thresh,
        down_thresh
    ):
        """Quickly identify the X[0] as a peak or valley."""
        x_0 = X[0]
        max_x = x_0
        max_t = 0
        min_x = x_0
        min_t = 0
        up_thresh += 1
        down_thresh += 1

        PEAK, VALLEY = 1, -1

        for t in range(1, len(X)):
            x_t = X[t]

            if x_t / min_x >= up_thresh:
                return VALLEY if min_t == 0 else PEAK

            if x_t / max_x <= down_thresh:
                return PEAK if max_t == 0 else VALLEY

            if x_t > max_x:
                max_x = x_t
                max_t = t

            if x_t < min_x:
                min_x = x_t
                min_t = t

        t_n = len(X)-1
        return VALLEY if x_0 < X[t_n] else PEAK

    ### Zig zag indicator (peak_valley_pivots_candlestick)
    def compute_zig_zag(
        self,
        close,
        high,
        low,
        up_thresh,
        down_thresh
    ):
        """
        Finds the peaks and valleys of a series of HLC (open is not necessary).
        TR: This is modified peak_valley_pivots function in order to find peaks and valleys for OHLC.
        Parameters
        ----------
        close : This is series with closes prices.
        high : This is series with highs  prices.
        low : This is series with lows prices.
        up_thresh : The minimum relative change necessary to define a peak.
        down_thesh : The minimum relative change necessary to define a valley.
        Returns
        -------
        an array with 0 indicating no pivot and -1 and 1 indicating valley and peak
        respectively
        Using Pandas
        ------------
        For the most part, close, high and low may be a pandas series. However, the index must
        either be [0,n) or a DateTimeIndex. Why? This function does X[t] to access
        each element where t is in [0,n).
        The First and Last Elements
        ---------------------------
        The first and last elements are guaranteed to be annotated as peak or
        valley even if the segments formed do not have the necessary relative
        changes. This is a tradeoff between technical correctness and the
        propensity to make mistakes in data analysis. The possible mistake is
        ignoring data outside the fully realized segments, which may bias analysis.
        """
        if down_thresh > 0:
            raise ValueError('The down_thresh must be negative.')

        initial_pivot = self._identify_initial_pivot(close, up_thresh, down_thresh)

        t_n = len(close)
        pivots = np.zeros(t_n, dtype='i1')
        pivots[0] = initial_pivot

        # Adding one to the relative change thresholds saves operations. Instead
        # of computing relative change at each point as x_j / x_i - 1, it is
        # computed as x_j / x_1. Then, this value is compared to the threshold + 1.
        # This saves (t_n - 1) subtractions.
        up_thresh += 1
        down_thresh += 1

        trend = -initial_pivot
        last_pivot_t = 0
        last_pivot_x = close[0]
        for t in range(1, len(close)):

            if trend == -1:
                x = low[t]
                r = x / last_pivot_x
                if r >= up_thresh:
                    pivots[last_pivot_t] = trend#
                    trend = 1
                    #last_pivot_x = x
                    last_pivot_x = high[t]
                    last_pivot_t = t
                elif x < last_pivot_x:
                    last_pivot_x = x
                    last_pivot_t = t
            else:
                x = high[t]
                r = x / last_pivot_x
                if r <= down_thresh:
                    pivots[last_pivot_t] = trend
                    trend = -1
                    #last_pivot_x = x
                    last_pivot_x = low[t]
                    last_pivot_t = t
                elif x > last_pivot_x:
                    last_pivot_x = x
                    last_pivot_t = t

        if last_pivot_t == t_n-1:
            pivots[last_pivot_t] = trend
        elif pivots[t_n-1] == 0:
            pivots[t_n-1] = trend

        self.selected_zig_zag_data['pivots'] = pivots
        self.selected_zig_zag_data['pivot_price'] = np.nan  # This line clears old pivot prices
        self.selected_zig_zag_data.loc[self.selected_zig_zag_data['pivots'] == 1, 'pivot_price'] = self.selected_zig_zag_data.high
        self.selected_zig_zag_data.loc[self.selected_zig_zag_data['pivots'] == -1, 'pivot_price'] = self.selected_zig_zag_data.low

        ### Fill missing values of zig zag data
        self.compute_and_update_missing_values_of_zig_zag_data()

    ### Compute and update missing values of zig zag indicator for plotting
    def compute_and_update_missing_values_of_zig_zag_data(
        self
    ):
        data_privot_price = self.selected_zig_zag_data[["pivot_price", "date_id"]].copy()
        data_privot_price_without_missing_values = data_privot_price[~data_privot_price.pivot_price.isna()].copy() # Drop missing values

        for i in range(1, len(data_privot_price_without_missing_values)):
            previous_date_id = data_privot_price_without_missing_values.date_id[i-1]
            current_date_id = data_privot_price_without_missing_values.date_id[i]
            diff_date_id = current_date_id-previous_date_id

            previous_pivot_price = data_privot_price_without_missing_values.pivot_price[i-1]
            current_pivot_price = data_privot_price_without_missing_values.pivot_price[i]
            
            if diff_date_id >= 2:
                ### Compute "m (slope)" and "y-intercept"
                m = (current_pivot_price-previous_pivot_price) / (current_date_id-previous_date_id)
                y = data_privot_price_without_missing_values.loc[data_privot_price_without_missing_values.date_id==previous_date_id, 'pivot_price'].values[0]
                x = data_privot_price_without_missing_values.loc[data_privot_price_without_missing_values.date_id==previous_date_id, 'date_id'].values[0]
                y_intercept = y - (m*x)

                ### Fill missing values
                for missing_value_position in range(previous_date_id+1, current_date_id):
                    self.selected_zig_zag_data.loc[self.selected_zig_zag_data.date_id==missing_value_position, 'pivot_price'] = (m*missing_value_position) + y_intercept
        
        ### Update
        self.zig_zag_data_of_multi_time_frames[self.selected_position_nth] = self.selected_zig_zag_data

    ### Compute EMA
    def compute_ema(self):
        fast_ema = ta.ema(self.selected_existing_data.close, self.n_fast_ema)[-1]
        slow_ema = ta.ema(self.selected_existing_data.close, self.n_slow_ema)[-1]

        ### Update
        self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, f"ema_{self.n_fast_ema}"] = fast_ema
        self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, f"ema_{self.n_slow_ema}"] = slow_ema

    ### Search AB interfaces
    def search_ab_interfaces(
        self
    ):
        fast_ema = self.selected_all_new_data[f"ema_{self.n_fast_ema}"].iloc[-1]
        slow_ema = self.selected_all_new_data[f"ema_{self.n_slow_ema}"].iloc[-1]

        ### Select AB interface
        if self.selected_round_nth == 0:
            if fast_ema > slow_ema:
                self.IsInterface = 'A'
            elif fast_ema < slow_ema:
                self.IsInterface = 'B'
            else:
                assert False, "fast_ema == slow_ema"

        ### Update
        self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'interface'] = self.IsInterface + f"_{self.cycle_nth}"

    ### Search EMA cutting down
    def search_ema_cutting_down(self):
        if len(self.selected_all_new_data) <= 1:
            IsEMACutting = np.nan
            cutting_deg = np.nan
            self.IsEMACuttingDown = np.nan
            
        else: # len(self.selected_all_new_data) >= 2
            fast_ema_line = self.selected_all_new_data[f"ema_{self.n_fast_ema}"].iloc[-2:].values
            slow_ema_line = self.selected_all_new_data[f"ema_{self.n_slow_ema}"].iloc[-2:].values
            IsEMACutting = np.diff(np.sign(fast_ema_line- slow_ema_line))[0] == -2 # Cutting=-2, Not cutting= ### [0] to get a value, -2 to convert number to bool
            cutting_deg = math.degrees(math.atan(np.diff(fast_ema_line)))

            self.IsEMACuttingDown = 0
            if IsEMACutting == True and cutting_deg<0:
                self.IsEMACuttingDown = 1
                self.ema_cutting_down_time = self.current_time_of_multi_time_frames

                self.cycle_nth += 1

        ### Update
        self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsEMACutting'] = IsEMACutting
        self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'cutting_deg'] = cutting_deg
        self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsEMACuttingDown'] = self.IsEMACuttingDown

        if self.IsEMACuttingDown == 1:
            self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'cutting_down_time'] = self.ema_cutting_down_time

    def compute_pivots_for_plotting(self):
        self.selected_zig_zag_data["pivot_ll"] = np.nan
        self.selected_zig_zag_data.loc[self.selected_zig_zag_data.pivots==-2, 'pivot_ll'] = self.selected_zig_zag_data.loc[self.selected_zig_zag_data.pivots==-2, 'low']
        self.selected_zig_zag_data["pivot_hl"] = np.nan
        self.selected_zig_zag_data.loc[self.selected_zig_zag_data.pivots==-1, 'pivot_hl'] = self.selected_zig_zag_data.loc[self.selected_zig_zag_data.pivots==-1, 'low']
        self.selected_zig_zag_data["pivot_hh"] = np.nan
        self.selected_zig_zag_data.loc[self.selected_zig_zag_data.pivots==2, 'pivot_hh'] = self.selected_zig_zag_data.loc[self.selected_zig_zag_data.pivots==2, 'high']
        self.selected_zig_zag_data["pivot_lh"] = np.nan
        self.selected_zig_zag_data.loc[self.selected_zig_zag_data.pivots==1, 'pivot_lh'] = self.selected_zig_zag_data.loc[self.selected_zig_zag_data.pivots==1, 'high']

        self.selected_zig_zag_data["pivot_buy_signal"] = np.nan
        self.selected_zig_zag_data.loc[self.selected_all_new_data.status=='buy', 'pivot_buy_signal'] = self.selected_zig_zag_data.loc[self.selected_all_new_data.status=='buy', 'low']
        self.selected_zig_zag_data["pivot_sell_signal"] = np.nan
        self.selected_zig_zag_data.loc[self.selected_all_new_data.status=='sell', 'pivot_sell_signal'] = self.selected_zig_zag_data.loc[self.selected_all_new_data.status=='sell', 'high']

    def search_ll_and_hl(self):
        self.IsLL = 0
        self.IsHL = 0

        if self.n_negative_pivots >= 1:
            self.IsLL = 1
            
            if self.n_negative_pivots == 1:
                self.ll_time = self.data_negative_pivots[self.data_negative_pivots.low==self.data_negative_pivots.low.min()].index[0]
                self.ll_value = self.data_negative_pivots.loc[self.ll_time, 'low']

            elif self.n_negative_pivots >= 2:
                self.IsHL = 1
                self.previous_negative_pivot_time = self.data_negative_pivots.index[-2]
                self.current_negative_pivot_time = self.data_negative_pivots.index[-1]
                self.previous_negative_pivot_value = self.data_negative_pivots.low[-2]
                self.current_negative_pivot_value = self.data_negative_pivots.low[-1]

                if self.current_negative_pivot_value < self.previous_negative_pivot_value:
                    self.ll_time = self.current_negative_pivot_time
                    self.ll_value = self.current_negative_pivot_value
                    self.hl_time = self.previous_negative_pivot_time
                    self.hl_value = self.previous_negative_pivot_value
                elif self.current_negative_pivot_value > self.previous_negative_pivot_value:
                    self.ll_time = self.previous_negative_pivot_time
                    self.ll_value = self.previous_negative_pivot_value
                    self.hl_time = self.current_negative_pivot_time
                    self.hl_value = self.current_negative_pivot_value
                else:
                    self.IsLL = 0
                    self.IsHL = 0

                # print(f"self.ll_value: {self.ll_value}, self.ll_time: {self.ll_time}")
                # print(f"self.hl_value: {self.hl_value}, self.hl_time: {self.hl_time}")

        ### Update
        self.selected_all_new_data.loc[self.selected_all_new_data.index==self.current_time_of_multi_time_frames, 'IsLL'] = self.IsLL
        self.selected_all_new_data.loc[self.selected_all_new_data.index==self.current_time_of_multi_time_frames, 'IsHL'] = self.IsHL

        if self.IsLL == 1:
            self.selected_all_new_data.loc[self.selected_all_new_data.index==self.current_time_of_multi_time_frames, 'll_time'] = self.ll_time
            self.selected_all_new_data.loc[self.selected_all_new_data.index==self.current_time_of_multi_time_frames, 'll_value'] = self.ll_value
            
            self.selected_zig_zag_data.loc[self.selected_zig_zag_data.index==self.ll_time, 'pivots'] = -2

        if self.IsHL == 1:
            self.selected_all_new_data.loc[self.selected_all_new_data.index==self.current_time_of_multi_time_frames, 'hl_time'] = self.hl_time
            self.selected_all_new_data.loc[self.selected_all_new_data.index==self.current_time_of_multi_time_frames, 'hl_value'] = self.hl_value

            if self.current_negative_pivot_value < self.previous_negative_pivot_value:
                self.selected_zig_zag_data.loc[(self.selected_zig_zag_data.index<self.ll_time)*(self.selected_zig_zag_data.pivots==-2), 'pivots'] = -1  # -1: Because found new ll

    def search_hh_and_lh(self):
        self.IsHH = 0
        self.IsLH = 0

        if self.n_positive_pivots >= 1:
            self.IsHH = 1
            
            if self.n_positive_pivots == 1:
                self.hh_time = self.data_positive_pivots[self.data_positive_pivots.high==self.data_positive_pivots.high.max()].index[0]
                self.hh_value = self.data_positive_pivots.loc[self.hh_time, 'high']
                
            elif self.n_positive_pivots >= 2:
                self.IsLH = 1
                self.previous_positive_pivot_time = self.data_positive_pivots.index[-2]
                self.previous_positive_pivot_value = self.data_positive_pivots.high[-2]
                self.current_positive_pivot_time = self.data_positive_pivots.index[-1]
                self.current_positive_pivot_value = self.data_positive_pivots.high[-1]

                if self.current_positive_pivot_value > self.previous_positive_pivot_value:
                    self.hh_time = self.current_positive_pivot_time
                    self.hh_value = self.current_positive_pivot_value
                    self.lh_time = self.previous_positive_pivot_time
                    self.lh_value = self.previous_positive_pivot_value
                elif self.current_positive_pivot_value < self.previous_positive_pivot_value:
                    self.hh_time = self.previous_positive_pivot_time
                    self.hh_value = self.previous_positive_pivot_value
                    self.lh_time = self.current_positive_pivot_time
                    self.lh_value = self.current_positive_pivot_value
                else:
                    self.IsHH = 0
                    self.IsLH = 0

                # print(f"self.hh_value: {self.hh_value}, self.hh_time: {self.hh_time}")
                # print(f"self.lh_value: {self.lh_value}, self.lh_time: {self.lh_time}")

        ### Update
        self.selected_all_new_data.loc[self.selected_all_new_data.index==self.current_time_of_multi_time_frames, 'IsHH'] = self.IsHH
        self.selected_all_new_data.loc[self.selected_all_new_data.index==self.current_time_of_multi_time_frames, 'IsLH'] = self.IsLH

        if self.IsHH == 1:
            self.selected_all_new_data.loc[self.selected_all_new_data.index==self.current_time_of_multi_time_frames, 'hh_time'] = self.hh_time
            self.selected_all_new_data.loc[self.selected_all_new_data.index==self.current_time_of_multi_time_frames, 'hh_value'] = self.hh_value
            
            self.selected_zig_zag_data.loc[self.selected_zig_zag_data.index==self.hh_time, 'pivots'] = 2

        if self.IsLH == 1:
            self.selected_all_new_data.loc[self.selected_all_new_data.index==self.current_time_of_multi_time_frames, 'lh_time'] = self.lh_time
            self.selected_all_new_data.loc[self.selected_all_new_data.index==self.current_time_of_multi_time_frames, 'lh_value'] = self.lh_value

            if self.current_positive_pivot_value > self.previous_positive_pivot_value:
                self.selected_zig_zag_data.loc[(self.selected_zig_zag_data.index<self.hh_time)*(self.selected_zig_zag_data.pivots==2), 'pivots'] = 1 # 1: Because found new hh
    
    ### *** Buy signal ***
    def sg_tf_hl(self):
        if self.IsHL==1 and self.IsHH==1 and self.IsLL==1 and self.IsLH==1 and self.IsSellSignal == 0:
            if self.hl_time > self.hh_time and self.hh_time > self.ll_time and self.ll_time > self.lh_time:
                self.IsBuySignal = 1
                self.IsOccur = "LL -> HH -> HL"
            else:
                self.IsBuySignal = 0
        else:
            self.IsBuySignal = 0

    

    ### *** Sell signal ***
    def sg_tf_lh(self): # [V.1] There is LH.
        if self.IsLH==1 and self.IsHH==1 and self.IsLL==1 and self.IsHL==1:
            if self.lh_time > self.hl_time and self.hl_time > self.hh_time and self.hh_time > self.ll_time:
                self.IsSellSignal = 1
                self.IsOccur = "LL -> HH -> LH"
            elif self.lh_time > self.ll_time and self.ll_time > self.hh_time and self.hh_time > self.hl_time:
                self.IsSellSignal = 1
                self.IsOccur = "HH -> LL -> LH"
            else:
                self.IsSellSignal = 0
        else:
            self.IsSellSignal = 0

    def sg_tf_ema_crossunder(self): # [V.2] There is EMA crossunder.
        if self.IsEMACuttingDown == 1:
            self.IsSellSignal = 1
            self.IsOccur = "EMA cutting down"
        else:
            self.IsSellSignal = 0

    def sg_tf_lh_or_ema_crossunder(self): # [V.3] There are LH or EMA crossunder.
        if self.IsLH==1 and self.IsHH==1 and self.IsLL==1 and self.IsHL==1:
            if self.lh_time > self.hl_time and self.hl_time > self.hh_time and self.hh_time > self.ll_time:
                self.IsSellSignal = 1
                self.IsOccur = "LL -> HH -> LH"
            elif self.lh_time > self.ll_time and self.ll_time > self.hh_time and self.hh_time > self.hl_time:
                self.IsSellSignal = 1
                self.IsOccur = "HH -> LL -> LH"
            else:
                self.IsSellSignal = 0
        elif self.IsEMACuttingDown == 1:
            self.IsSellSignal = 1
            self.IsOccur = "EMA cutting down"
        else:
            self.IsSellSignal = 0

    def sg_tf_ema_crossunder_and_lh(self): # [V.4] There is EMA crossunder then LH.
        pseudo_sell_signal_data = self.selected_all_new_data.loc[self.selected_all_new_data.IsEMACuttingDown==1]
        n_pseudo_sell_signal = len(pseudo_sell_signal_data)

        if n_pseudo_sell_signal >= 1:
            if self.IsLH==1 and self.IsHH==1 and self.IsLL==1 and self.IsHL==1:
                if self.lh_time > self.hl_time and self.hl_time > self.hh_time and self.hh_time > self.ll_time:
                    self.IsSellSignal = 1
                    self.IsOccur = "LL -> HH -> LH"
                elif self.lh_time > self.ll_time and self.ll_time > self.hh_time and self.hh_time > self.hl_time:
                    self.IsSellSignal = 1
                    self.IsOccur = "HH -> LL -> LH"
                else:
                    self.IsSellSignal = 0
            else:
                self.IsSellSignal = 0
        else:
            self.IsSellSignal = 0

    # def sg_tf_lh_and_ema_crossunder(self): # There is LH then EMA crossunder.
    #     if self.IsLH==1 and self.IsHH==1 and self.IsLL==1 and self.IsHL==1:
    #         if (self.lh_time > self.hl_time and self.hl_time > self.hh_time and self.hh_time > self.ll_time) or (self.lh_time > self.ll_time and self.ll_time > self.hh_time and self.hh_time > self.hl_time):
    #             IsPseudoSellSignal = 1
    #         else:
    #             IsPseudoSellSignal = 0
    #     else:
    #         IsPseudoSellSignal = 0

    #     ### Update psuedo sell signal
    #     self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsPseudoSellSignal'] = IsPseudoSellSignal

    #     if self.IsEMACuttingDown == 1:
    #         pseudo_sell_signal_data = self.selected_all_new_data.loc[self.selected_all_new_data.IsPseudoSellSignal==1]
    #         n_pseudo_sell_signal = len(pseudo_sell_signal_data)
            
    #         if n_pseudo_sell_signal >= 1:
    #             self.IsSellSignal = 1
    #         else:
    #             self.IsSellSignal = 0
    #     else:
    #         self.IsSellSignal = 0

    def strategy(self):
        ### Determine zig zag data to search LL, HH, HL or LH
        self.selected_zig_zag_data = self.zig_zag_data_of_multi_time_frames[self.selected_position_nth]
        self.data_positive_pivots = self.selected_zig_zag_data[(self.selected_zig_zag_data.pivots == 1)*(self.selected_zig_zag_data.interface == f"{self.IsInterface}_{self.cycle_nth}")]
        self.data_negative_pivots = self.selected_zig_zag_data[(self.selected_zig_zag_data.pivots == -1)*(self.selected_zig_zag_data.interface == f"{self.IsInterface}_{self.cycle_nth}")]
        self.n_positive_pivots = len(self.data_positive_pivots)
        self.n_negative_pivots = len(self.data_negative_pivots)

        if self.selected_round_nth == 0:
            self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsBuySignal'] = 0
            self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsSellSignal'] = 0
            self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'status'] = "waiting"

        ### Search LL and HL
        self.search_ll_and_hl()
        ### Search HH and LH
        self.search_hh_and_lh()

        ### Search buy signal
        if self.buy_strategy == "sg_tf_hl":
            self.sg_tf_hl()

        ### Search sell signal
        if self.sell_strategy == 'sg_tf_lh':
            self.sg_tf_lh()
        elif self.sell_strategy == 'sg_tf_ema_crossunder':
            self.sg_tf_ema_crossunder()
        elif self.sell_strategy == 'sg_tf_lh_or_ema_crossunder':
            self.sg_tf_lh_or_ema_crossunder()
        elif self.sell_strategy == 'sg_tf_ema_crossunder_and_lh':
            self.sg_tf_ema_crossunder_and_lh()
        
        if pd.to_datetime(self.current_time.strftime('%H:%M:%S')) >= pd.to_datetime('15:54:59'):
            self.IsBuySignal = 0
            self.IsSellSignal = 1
            self.IsOccur = "Less than 5 minutes remaining."

        # ### Update buy signal
        # self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsBuySignal'] = self.IsBuySignal
        # ### Update sell signal
        # self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsSellSignal'] = self.IsSellSignal
        
        ### Update buy signal
        self.log_data.loc[self.current_time, 'IsBuySignal'] = self.IsBuySignal
        ### Update sell signal
        self.log_data.loc[self.current_time, 'IsSellSignal'] = self.IsSellSignal

        # print(f"self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsBuySignal']: {self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsBuySignal']}")
        # print(f"self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsSellSignal']: {self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsSellSignal']}")
        # print(f"self.IsEMACuttingDown: {self.IsEMACuttingDown}")

    def check_and_update_missing_times(self):
        try:
            n_missing_times = (self.all_new_data.index[-1]-self.all_new_data.index[-2]).seconds - 1

            if n_missing_times >= 1:
                for m_t in range(n_missing_times):
                    missing_time = self.all_new_data.index[-2] + relativedelta(seconds=1)
                    missing_data = self.all_new_data.loc[self.all_new_data.index<missing_time].tail(14).mean().to_frame().T
                    missing_data.index = [missing_time] # Change index
                    self.all_new_data = pd.concat([self.all_new_data, missing_data]) # Update all new data
                    self.all_new_data.sort_index(inplace=True)  
        except:
            pass

    def update_log_data(self):
        dict_re_column_names = {col_name: f"{col_name}__{self.n_time_frames}" for col_name in self.selected_all_new_data.columns}
        selected_all_new_data_for_log = self.selected_all_new_data.tail(1).rename(columns=dict_re_column_names)
        selected_all_new_series_for_log = selected_all_new_data_for_log.squeeze(axis=0)
        if len(self.log_data) == 0:
            self.log_data = pd.concat([self.log_data, selected_all_new_data_for_log], axis=0)
        else:
            try:
                if selected_all_new_data_for_log.index[0] not in self.log_data.index:
                    self.log_data = pd.concat([self.log_data, selected_all_new_data_for_log], axis=0)
                else:
                    self.log_data = pd.concat([self.log_data, selected_all_new_data_for_log], axis=1)
            except:
                self.log_data.loc[selected_all_new_series_for_log.name] = selected_all_new_series_for_log

    def compute_nav(self):
        maker_fees = 0.002 # usd per share
        taker_fees = 0.002 # usd per share

        self.log_data['_pct_change'] = self.log_data.open.pct_change()

        if self.round_nth == 0:
            self.log_data.loc[self.current_time, 'bullets'] = self.initial_cash
            self.log_data.loc[self.current_time, 'holding'] = 0
        else:
            self.previous_time = log_data.index[-2]

            if log_data.loc[self.previous_time, 'status'] == 'waiting':
                self.log_data[self.current_time, 'bullets'] = self.log_data[self.previous_time, 'bullets']
                self.log_data[self.current_time, 'holding'] = self.log_data[self.previous_time, 'bullets']

        # if self.round_nth == 0:
        #     self.nav_data.loc[self.current_time, 'bullets'] = self.initial_cash
        #     self.nav_data.loc[self.current_time, 'holding'] = 0
        #     self.nav_data.loc[self.current_time, 'status'] = 'waiting'
        # else:
        #     previous_bullets = self.nav_data.bullets[-2]
        #     self.previous_time = self.nav_data.index[-2]
        #     try:
        #         if self.log_data[f"IsBuySignal__{self.list_n_time_frames[0]}"][-1] == 1:
        #             if self.nav_data.loc[self.previous_time, 'status'] == 'waiting':
        #                 self.nav_data.loc[self.current_time, 'bullets'] = previous_bullets
        #                 self.nav_data.loc[self.current_time, 'holding'] = self.nav_data.loc[self.previous_time, 'holding']        
        #                 self.nav_data.loc[self.current_time, 'status'] = 'ready_to_buy'

        #             elif self.nav_data.loc[self.previous_time, 'status'] == 'ready_to_buy':
        #                 if previous_bullets-self.initial_cash >= 0:
        #                     commission = (self.initial_cash/self.nav_data.loc[self.current_time, 'open']) * maker_fees
        #                     self.nav_data.loc[self.current_time, 'bullets'] = previous_bullets-self.initial_cash
        #                     self.nav_data.loc[self.current_time, 'holding'] = self.initial_cash - commission
        #                     self.nav_data.loc[self.current_time, 'status'] = 'buy'
        #                     self.reference_cash_at_the_buy_timing = self.initial_cash

        #                     self.nav_data.loc[self.current_time, 'commission'] = commission
        #                 else:
        #                     commission = (previous_bullets/self.nav_data.loc[self.current_time, 'open']) * maker_fees
        #                     self.nav_data.loc[self.current_time, 'bullets'] = 0
        #                     self.nav_data.loc[self.current_time, 'holding'] = previous_bullets - commission
        #                     self.nav_data.loc[self.current_time, 'status'] = 'buy'
        #                     self.reference_cash_at_the_buy_timing = previous_bullets

        #                     self.nav_data.loc[self.current_time, 'commission'] = commission

        #             elif self.nav_data.loc[self.previous_time, 'status'] == 'buy' or self.nav_data.loc[self.previous_time, 'status'] == 'holding':
        #                 self.nav_data.loc[self.current_time, 'bullets'] = previous_bullets
        #                 self.nav_data.loc[self.current_time, 'holding'] = self.nav_data.loc[self.previous_time, 'holding'] * (self.nav_data.loc[self.current_time, '_pct_change'] + 1)
        #                 self.nav_data.loc[self.current_time, 'status'] = 'holding'
        #                 pnl = self.nav_data.loc[self.current_time, 'holding'] - self.reference_cash_at_the_buy_timing
        #                 self.pnl_pct_change = (self.nav_data.loc[self.current_time, 'holding']/self.reference_cash_at_the_buy_timing) - 1

        #         elif self.log_data[f"status__{self.list_n_time_frames[0]}"][-1] == 'buy' and (self.nav_data.loc[self.previous_time, 'status'] == 'holding'):
        #             self.nav_data.loc[self.current_time, 'bullets'] = previous_bullets
        #             self.nav_data.loc[self.current_time, 'holding'] = self.nav_data.loc[self.previous_time, 'holding'] * (self.nav_data.loc[self.current_time, '_pct_change'] + 1)
        #             self.nav_data.loc[self.current_time, 'status'] = 'holding'
        #             pnl = self.nav_data.loc[self.current_time, 'holding'] - self.reference_cash_at_the_buy_timing
        #             self.pnl_pct_change = (self.nav_data.loc[self.current_time, 'holding']/self.reference_cash_at_the_buy_timing) - 1

        #         elif self.log_data[f"status__{self.list_n_time_frames[0]}"][-1] == 'holding' and self.nav_data.loc[self.previous_time, 'status'] == 'holding' and self.log_data[f"IsSellSignal__{self.list_n_time_frames[0]}"][-1] != 1:
        #             self.nav_data.loc[self.current_time, 'bullets'] = previous_bullets
        #             self.nav_data.loc[self.current_time, 'holding'] = self.nav_data.loc[self.previous_time, 'holding'] * (self.nav_data.loc[self.current_time, '_pct_change'] + 1)
        #             self.nav_data.loc[self.current_time, 'status'] = 'holding'
        #             pnl = self.nav_data.loc[self.current_time, 'holding'] - self.reference_cash_at_the_buy_timing
        #             self.pnl_pct_change = (self.nav_data.loc[self.current_time, 'holding']/self.reference_cash_at_the_buy_timing) - 1

        #         elif (self.log_data[f"IsSellSignal__{self.list_n_time_frames[0]}"][-1] == 1 and self.nav_data.loc[self.previous_time, 'status'] != 'sell' and self.nav_data.loc[self.previous_time, 'status'] != 'waiting'):
        #             if self.nav_data.loc[self.previous_time, 'status'] == 'holding':
        #                 self.nav_data.loc[self.current_time, 'bullets'] = previous_bullets
        #                 self.nav_data.loc[self.current_time, 'holding'] = self.nav_data.loc[self.previous_time, 'holding'] * (self.nav_data.loc[self.current_time, '_pct_change'] + 1)
        #                 self.nav_data.loc[self.current_time, 'status'] = 'ready_to_sell'
        #             elif self.nav_data.loc[self.previous_time, 'status'] == 'ready_to_sell':
        #                 commission = (self.nav_data.loc[self.previous_time, 'holding']/self.nav_data.loc[self.current_time, 'open']) * taker_fees
        #                 self.nav_data.loc[self.current_time, 'holding'] = 0
        #                 self.nav_data.loc[self.current_time, 'bullets'] = self.nav_data.loc[self.previous_time, 'bullets'] + self.nav_data.loc[self.previous_time, 'holding'] * (self.nav_data.loc[self.current_time, '_pct_change'] + 1) - commission
        #                 self.nav_data.loc[self.current_time, 'status'] = 'sell'
        #                 pnl = self.nav_data.loc[self.current_time, 'bullets'] - self.reference_cash_at_the_buy_timing
        #                 self.pnl_pct_change = (self.nav_data.loc[self.current_time, 'bullets']/self.reference_cash_at_the_buy_timing) - 1

        #                 self.nav_data.loc[self.current_time, 'commission'] = commission

        #         elif self.log_data[f"status__{self.list_n_time_frames[0]}"][-1] == 'sell' and (self.nav_data.loc[self.previous_time, 'status'] == 'holding'):
        #             self.nav_data.loc[self.current_time, 'bullets'] = previous_bullets
        #             self.nav_data.loc[self.current_time, 'holding'] = self.nav_data.loc[self.previous_time, 'holding'] * (self.nav_data.loc[self.current_time, '_pct_change'] + 1)
        #             self.nav_data.loc[self.current_time, 'status'] = 'ready_to_sell'
        #             pnl = self.nav_data.loc[self.current_time, 'bullets'] - self.reference_cash_at_the_buy_timing
        #             self.pnl_pct_change = (self.nav_data.loc[self.current_time, 'bullets']/self.reference_cash_at_the_buy_timing) - 1

        #         elif self.nav_data.loc[self.previous_time, 'status'] == 'ready_to_sell':
        #             commission = (self.nav_data.loc[self.previous_time, 'holding']/self.nav_data.loc[self.current_time, 'open']) * taker_fees
        #             self.nav_data.loc[self.current_time, 'holding'] = 0
        #             self.nav_data.loc[self.current_time, 'bullets'] = self.nav_data.loc[self.previous_time, 'bullets'] + self.nav_data.loc[self.previous_time, 'holding'] * (self.nav_data.loc[self.current_time, '_pct_change'] + 1) - commission
        #             self.nav_data.loc[self.current_time, 'status'] = 'sell'
        #             pnl = self.nav_data.loc[self.current_time, 'bullets'] - self.reference_cash_at_the_buy_timing
        #             self.pnl_pct_change = (self.nav_data.loc[self.current_time, 'bullets']/self.reference_cash_at_the_buy_timing) - 1
                    
        #             self.nav_data.loc[self.current_time, 'commission'] = commission
                
        #         else: # self.log_data[f"status__{self.list_n_time_frames[0]}"][-1] == 'waiting'
        #             self.nav_data.loc[self.current_time, 'bullets'] = previous_bullets
        #             self.nav_data.loc[self.current_time, 'holding'] = self.nav_data.loc[self.previous_time, 'holding']
        #             self.nav_data.loc[self.current_time, 'status'] = 'waiting'

        #     except: # Incase, There're no multi time frames data
        #         self.nav_data.loc[self.current_time, 'bullets'] = previous_bullets
        #         self.nav_data.loc[self.current_time, 'holding'] = self.nav_data.loc[self.previous_time, 'holding']
        #         self.nav_data.loc[self.current_time, 'status'] = self.nav_data.loc[self.previous_time, 'status']

        # ### Update
        # self.nav_data.loc[self.current_time, 'nav'] = self.nav_data.loc[self.current_time, 'bullets'] + self.nav_data.loc[self.current_time, 'holding']

        # try:
        #     self.nav_data.loc[self.current_time, 'pnl'] = pnl
        #     self.nav_data.loc[self.current_time, 'pnl_pct_change'] = self.pnl_pct_change
        # except:
        #     pass

    def verbose(self):
        if self.show_verbose:
            print(f"({self.round_nth}) current time: {self.current_time}")
            print(f"o: {np.round(self.nav_data.loc[self.current_time, 'open'], 4)}, h: {np.round(self.nav_data.loc[self.current_time, 'high'], 4)}, l: {np.round(self.nav_data.loc[self.current_time, 'low'], 4)}, c: {np.round(self.nav_data.loc[self.current_time, 'close'], 4)}, pct_change: {np.round(self.nav_data.loc[self.current_time, '_pct_change']*100, 4)}%")
            try:
                # print(f"self.current_time_of_multi_time_frames: {self.current_time_of_multi_time_frames}")
                print(f'IsBuySignal: {self.log_data.IsBuySignal__15[-1]}')
                print(f'IsSellSignal: {self.log_data.IsSellSignal__15[-1]}')
                print(f'IsEMACuttingDown: {self.log_data.IsEMACuttingDown__15[-1]}')
                if self.IsBuySignal == 1 or self.IsSellSignal == 1 or self.IsEMACuttingDown:
                    print(f"Occur: {self.IsOccur}")
            except:
                pass

            print(f"Status: {self.nav_data.loc[self.current_time, 'status']}")
            # print(f"Bullets: {self.nav_data.loc[self.current_time, 'bullets']}")
            # print(f"Holding: {self.nav_data.loc[self.current_time, 'holding']}")
            # try:
            #     print(f"Commission: {commission}")
            # except:
            #     pass
            # try:
            #     print(f"PNL: {np.round(pnl, 4)}")
            #     print(f"PNL pct: {np.round(self.pnl_pct_change*100, 4)}%")
            # except:
            #     pass
            print("-"*100)

    def check_and_update_status(self):
        # if self.selected_round_nth >= 1:
        #     if self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'IsBuySignal'] == 0 and self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'status']!="holding":
        #         if self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'IsSellSignal'] == 1 and self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'status'] == 'buy':
        #             self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'status'] = "sell"
        #         elif self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'IsSellSignal'] == 0 and self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'status'] == 'buy':
        #             self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'status'] = "holding"
        #         else:
        #             self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'status'] = "waiting"
            
        #     else: # self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'IsBuySignal'] == 1
        #         if self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'IsSellSignal'] == 0:
        #             if self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'status']=="waiting" and self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'status']!="holding":
        #                 self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'status'] = "buy"
                    
        #             elif self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'status']=="buy" or self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'status']=="holding":
        #                 self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'status'] = "holding"
                    
        #             # elif self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'status']=="cut_loss_at_the_same_time" or self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'status']=="cut_loss_at_the_other_time":
        #             #     self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'status'] = "waiting"

        #         else: # self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'IsSellSignal'] == 1
        #             if self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'status']=="buy" or self.selected_all_new_data.loc[self.previous_time_of_multi_time_frames, 'status']=="holding":
        #                 self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'status'] = "sell"
        if self.round_nth == 0:
            self.log_data.loc[self.current_time, 'status'] = 'waiting'
        else:
            try:
                if self.log_data.loc[self.previous_time, 'IsBuySignal'] == 0:
                    if self.log_data.loc[self.current_time, 'IsSellSignal'] == 1 and self.log_data.loc[self.current_time, 'status'] == 'holding':
                        self.log_data.loc[self.current_time, 'status'] = 'waiting'
                
                else: # self.log_data.loc[self.previous_time, 'IsBuySignal'] == 1
                    if self.log_data.loc[self.previous_time, 'IsSellSignal'] == 0:
                        if self.log_data.loc[self.previous_time, 'status'] == 'waiting':

            except:
                self.log_data.loc[self.current_time, 'status'] = 'waiting'



    def run_strategy(self):
        ### Update data
        self.existing_data = pd.concat([self.existing_data, self.new_data])
        self.all_new_data = pd.concat([self.all_new_data, self.new_data])

        self.current_time = self.new_data.index[-1]

        ### Check and update missing times
        self.check_and_update_missing_times()

        ### Update log_data
        self.log_data = pd.concat([self.log_data, self.all_new_data.tail(1)])

        ### Check and update the status
        self.check_and_update_status()

        ### Update log data
        self.compute_nav()


        for self.n_time_frames in self.list_n_time_frames:
            ### Append position nth
            self.selected_position_nth = self.search_update_position(self.n_time_frames)

            if len(self.all_new_data) % self.n_time_frames == 0:

                ### Convert new data to multi time frames
                self.convert_new_data_to_multi_time_frames()
                
                ### Update existing
                self.update_existing_data_of_multi_time_frames() # To compute EMA

                ### Selected ...
                self.selected_round_nth = self.round_nth_of_multi_time_frames[self.selected_position_nth]
                self.selected_existing_data = self.existing_data_of_multi_time_frames[self.selected_position_nth]
                self.selected_all_new_data = self.all_new_data_of_multi_time_frames[self.selected_position_nth]
                self.current_time_of_multi_time_frames = self.converted_new_data_of_multi_time_frames.index[0]
                # print(f"self.current_time_of_multi_time_frames: {self.current_time_of_multi_time_frames}")
                try:
                    self.previous_time_of_multi_time_frames = self.selected_all_new_data.index[-2]
                except:
                    pass

                ### Compute EMA
                self.compute_ema()

                ### Search AB interfaces
                self.search_ab_interfaces()

                ### Search EMA cutting down
                self.search_ema_cutting_down()

                ### Zig zag indicator (peak_valley_pivots_candlestick)
                self.selected_zig_zag_data = self.selected_all_new_data[['open', 'high', 'low', 'close', 'date_id', 'interface']].copy()
                self.compute_zig_zag(self.selected_zig_zag_data.close, self.selected_zig_zag_data.high, self.selected_zig_zag_data.low, self.up_thresh, self.down_thresh)

                ### *** Strategies ***
                self.strategy()

                ### Check and update the status
                # self.check_and_update_status()

                ### Plot
                # self.compute_pivots_for_plotting() # Compute pivots for plotting
                # self.plot()

                ### Update log data
                # self.update_log_data()

                print(f'----- self.n_time_frames: {self.n_time_frames} -----')

                self.round_nth_of_multi_time_frames[self.selected_position_nth] += 1

            else:
                if len(self.all_new_data) < self.n_time_frames:
                    self.time_in_multi_time_frames[self.selected_position_nth] = self.all_new_data.index[0]
                elif len(self.all_new_data)-1 % self.n_time_frames:
                    # print(self.all_new_data)
                    # print(f"self.round_nth_of_multi_time_frames[self.selected_position_nth]: {self.round_nth_of_multi_time_frames[self.selected_position_nth]}")
                    # print(f"self.n_time_frames*self.round_nth_of_multi_time_frames[self.selected_position_nth]: {self.n_time_frames*self.round_nth_of_multi_time_frames[self.selected_position_nth]}")
                    self.time_in_multi_time_frames[self.selected_position_nth] = self.all_new_data.index[self.n_time_frames*self.round_nth_of_multi_time_frames[self.selected_position_nth]]

            print(f"self.time_in_multi_time_frames[self.selected_position_nth]: {self.time_in_multi_time_frames[self.selected_position_nth]}")
            # print(f"self.time_in_multi_time_frames: {self.time_in_multi_time_frames}")

        ### Verbose
        self.verbose()

        ### Update round
        self.round_nth += 1