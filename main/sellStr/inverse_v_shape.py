def inverse_v_shape(self):
    if "inverse_v_shape" in self.list_sell_strategies:
        try:
            if self.log_data.loc[self.previous_time, f'TF{self.list_n_time_frames[0]}s__IsInverseVShape'] == 1:
                self.IsSellSignal = 1
            else:
                self.IsSellSignal = 0
        except:
            self.IsSellSignal = 0

        ### Update
        self.log_data.loc[self.current_time, 'IsSellSignal'] = self.IsSellSignal