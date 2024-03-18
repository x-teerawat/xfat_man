from _libs import *

def indicator_atr(self):
    atr_values = ta.atr(self.selected_existing_data.high, self.selected_existing_data.low, self.selected_existing_data.close, 14)

    ### Update
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, "atr"] = atr_values[-1]