def turtle_shell(self):
    if "turtle_shell" in self.list_buy_strategies:
        try:
            if self.log_data.loc[self.previous_time, f'TF{self.list_n_time_frames[0]}s__IsTurtleShell'] == 1:
                self.IsBuySignal = 1
            else:
                self.IsBuySignal = 0
        except:
            self.IsBuySignal = 0

        ### Update
        self.log_data.loc[self.current_time, 'IsBuySignal'] = self.IsBuySignal