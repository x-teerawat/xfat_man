def v_shape(self):
    if "v_shape" in self.list_buy_strategies:
        try:
            if self.log_data.loc[self.previous_time, f'TF{self.list_n_time_frames[0]}s__IsVShape'] == 1:
                self.IsBuySignal = 1
            else:
                self.IsBuySignal = 0
        except:
            self.IsBuySignal = 0

        ### Update
        self.log_data.loc[self.current_time, 'IsBuySignal'] = self.IsBuySignal