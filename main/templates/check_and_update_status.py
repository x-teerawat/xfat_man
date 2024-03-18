def check_and_update_status(self):
    if self.round_nth == 0:
        status = "waiting"
    else:
        if self.IsBuySignal == 1 and self.IsSellSignal == 0:
            if self.log_data.loc[self.previous_time, 'status'] == 'waiting' or self.log_data.loc[self.previous_time, 'status'] == 'sell':
                status = 'buy'
            else:
                status = 'holding'

        elif self.IsBuySignal == 0 and self.IsSellSignal == 0:
            if self.log_data.loc[self.previous_time, 'status'] == 'buy' or self.log_data.loc[self.previous_time, 'status'] == 'holding':
                status = 'holding'
            else: # self.log_data.loc[self.previous_time, 'status'] == 'waiting' or self.log_data.loc[self.previous_time, 'status'] == 'sell'
                status = 'waiting'

        else: # self.IsSellSignal == 1
            if self.log_data.loc[self.previous_time, 'status'] == 'buy' or self.log_data.loc[self.previous_time, 'status'] == 'holding':
                status = 'sell'
            else:
                status = 'waiting'

    ### Update a status
    self.log_data.loc[self.current_time, 'status'] = status

