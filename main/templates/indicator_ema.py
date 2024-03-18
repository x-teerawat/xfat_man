from _libs import *

def indicator_ema(self):
    fast_ema_value = ta.ema(self.selected_existing_data.close, self.n_fast_ema)[-1]
    slow_ema_value = ta.ema(self.selected_existing_data.close, self.n_slow_ema)[-1]
    # print(f"self.n_fast_ema, {self.n_fast_ema}")
    # print(f"self.n_slow_ema, {self.n_slow_ema}")
    # print(f"fast_ema_value, {fast_ema_value}")
    # print(f"slow_ema_value, {slow_ema_value}")

    ### Update
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, f"ema_{self.n_fast_ema}"] = fast_ema_value
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, f"ema_{self.n_slow_ema}"] = slow_ema_value
    