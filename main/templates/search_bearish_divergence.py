from _libs import *

def search_bearish_divergence(self):
    training_data = self.selected_all_new_data.tail(self.n_lags) # Training data

    try:
        idx = np.argsort(np.abs(training_data.rsi - training_data.rsi.max()))
        closest_idx = idx[0] # x_1
        second_closest_idx = idx[1] # x_2
        ### Slope
        price_slope = (training_data.high[second_closest_idx] - training_data.high[closest_idx]) / (second_closest_idx - closest_idx)
        rsi_slope = (training_data.rsi[second_closest_idx] - training_data.rsi[closest_idx]) / (second_closest_idx - closest_idx)

        if (price_slope>0 and rsi_slope<0) and (training_data.rsi[closest_idx]>=70 or training_data.rsi[second_closest_idx]>=70):
            self.IsBearishDivergence = 1
        else:
            self.IsBearishDivergence = 0

    except:
        self.IsBearishDivergence = 0

    ### Update
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsBearishDivergence'] = self.IsBearishDivergence