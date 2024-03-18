def search_ab_interfaces(self):
    # fast_ema = self.selected_all_new_data[f"ema_{min(self.list_n_ema)}"].iloc[-1]
    # slow_ema = self.selected_all_new_data[f"ema_{max(self.list_n_ema)}"].iloc[-1]

    if self.selected_round_nth == 0:
        if self.n_fast_ema > self.n_slow_ema:
            self.IsInterface = 'A'
        elif self.n_fast_ema < self.n_slow_ema:
            self.IsInterface = 'B'
        else:
            assert False, "fast_ema == slow_ema"

    print(f"self.IsInterface, {self.IsInterface}")

    ### Update
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'interface'] = self.IsInterface + f"_{self.cycle_nth}"


    