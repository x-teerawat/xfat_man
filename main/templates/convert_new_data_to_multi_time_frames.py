from _libs import *

def convert_new_data_to_multi_time_frames(self):
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
    self.existing_data_of_multi_time_frames[self.selected_position_nth] = pd.concat([self.existing_data_of_multi_time_frames[self.selected_position_nth], self.converted_new_data_of_multi_time_frames])
    self.all_new_data_of_multi_time_frames[self.selected_position_nth] = pd.concat([self.all_new_data_of_multi_time_frames[self.selected_position_nth], self.converted_new_data_of_multi_time_frames])