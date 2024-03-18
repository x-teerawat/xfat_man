from _libs import *

def indicator_rsi(self):
    rsi_value = ta.rsi(self.selected_existing_data.close, 14)[-1]

    ### Update
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, "rsi"] = rsi_value