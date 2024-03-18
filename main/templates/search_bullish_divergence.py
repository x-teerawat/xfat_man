from _libs import *

def search_bullish_divergence(self):
    training_data = self.selected_all_new_data.tail(self.n_lags) # Training data
    
    try:
        idx = np.argsort(np.abs(training_data.rsi - training_data.rsi.min()))
        closest_idx = idx[0] # x_1
        second_closest_idx = idx[1] # x_2
        ### Slope
        price_slope = (training_data.low[second_closest_idx] - training_data.low[closest_idx]) / (second_closest_idx - closest_idx)
        rsi_slope = (training_data.rsi[second_closest_idx] - training_data.rsi[closest_idx]) / (second_closest_idx - closest_idx)

        if (price_slope<0 and rsi_slope>0) and (training_data.rsi[closest_idx]<=30 or training_data.rsi[second_closest_idx]<=30):
            self.IsBullishDivergence = 1
        else:
            self.IsBullishDivergence = 0

    except:
        self.IsBullishDivergence = 0

    # print(f"self.IsBullishDivergence: {self.IsBullishDivergence}")

    ### Update
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsBullishDivergence'] = self.IsBullishDivergence