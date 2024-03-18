from _libs import *

def compute_angle(self):
    lookback = 4

    close_delta = self.selected_existing_data['close'] - self.selected_existing_data['close'].shift(lookback)
    close_angle_values = np.arctan(close_delta/ta.atr(self.selected_existing_data.high, self.selected_existing_data.low, self.selected_existing_data.close, lookback))*180/np.pi

    low_delta = self.selected_existing_data['low'] - self.selected_existing_data['low'].shift(lookback)
    low_angle_values = np.arctan(low_delta/ta.atr(self.selected_existing_data.high, self.selected_existing_data.low, self.selected_existing_data.close, lookback))*180/np.pi

    high_delta = self.selected_existing_data['high'] - self.selected_existing_data['high'].shift(lookback)
    high_angle_values = np.arctan(high_delta/ta.atr(self.selected_existing_data.high, self.selected_existing_data.low, self.selected_existing_data.close, lookback))*180/np.pi

    ### Update
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'close_angle'] = close_angle_values[-1]
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'low_angle'] = low_angle_values[-1]
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'high_angle'] = high_angle_values[-1]
