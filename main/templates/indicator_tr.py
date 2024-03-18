from _libs import *

def indicator_tr(self):
    tr_values = np.maximum.reduce([
        abs(self.selected_existing_data.high - self.selected_existing_data.low),
        abs(self.selected_existing_data.high - self.selected_existing_data.close.shift(1)),
        abs(self.selected_existing_data.low - self.selected_existing_data.close.shift(1))
    ])
    
    ### Update
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, "tr"] = tr_values[-1]
