def compute_nav(self):
    maker_fees = 0.002 # usd per share
    taker_fees = 0.002 # usd per share

    self.log_data['_pct_change'] = self.log_data.open.pct_change()

    if self.round_nth == 0:
        self.log_data.loc[self.current_time, 'bullets'] = self.initial_cash
        self.log_data.loc[self.current_time, 'holding'] = 0
        
    else:
        if self.log_data.status[-1] == 'waiting':
            self.log_data.loc[self.current_time, 'bullets'] = self.log_data.bullets[-2]
            self.log_data.loc[self.current_time, 'holding'] = self.log_data.holding[-2]

        elif self.log_data.status[-1] == 'buy':
            if self.log_data.bullets[-2]-self.initial_cash >= 0:
                commission = (self.initial_cash/self.log_data.open[-1]) * self.maker_fees

                self.log_data.loc[self.current_time, 'bullets'] = self.log_data.bullets[-2]-self.initial_cash
                self.log_data.loc[self.current_time, 'holding'] = self.initial_cash - commission

                self.log_data.loc[self.current_time, 'commission'] = commission
                self.reference_cash_at_the_buy_timing = self.initial_cash

            else:
                commission = (self.log_data.bullets[-2]/self.log_data.open[-1]) * self.maker_fees

                self.log_data.loc[self.current_time, 'bullets'] = 0
                self.log_data.loc[self.current_time, 'holding'] = self.log_data.bullets[-2] - commission

                self.log_data.loc[self.current_time, 'commission'] = commission
                self.reference_cash_at_the_buy_timing = self.log_data.bullets[-2]

        elif self.log_data.status[-1] == 'sell':
            commission = ((self.log_data.holding[-2]*(self.log_data._pct_change[-1]+1)) / self.log_data.open[-1]) * self.taker_fees

            self.log_data.loc[self.current_time, 'holding'] = 0
            self.log_data.loc[self.current_time, 'bullets'] = (self.log_data.holding[-2] * (self.log_data._pct_change[-1]+1) - commission) + self.log_data.bullets[-2]
            pnl = self.log_data.bullets[-1] - self.reference_cash_at_the_buy_timing
            self.pnl_pct_change = (self.log_data.bullets[-1]/self.reference_cash_at_the_buy_timing) - 1

            self.log_data.loc[self.current_time, 'commission'] = commission
            self.log_data.loc[self.current_time, 'pnl'] = pnl
            self.log_data.loc[self.current_time, 'pnl_pct_change'] = self.pnl_pct_change

        else: # self.log_data.status[-1] == 'holding'
            self.log_data.loc[self.current_time, 'bullets'] = self.log_data.bullets[-2]
            self.log_data.loc[self.current_time, 'holding'] = self.log_data.holding[-2] * (self.log_data._pct_change[-1]+1)
            pnl = self.log_data.holding[-1] - self.reference_cash_at_the_buy_timing
            self.pnl_pct_change = (self.log_data.holding[-1]/self.reference_cash_at_the_buy_timing) - 1
            
            self.log_data.loc[self.current_time, 'pnl'] = pnl
            self.log_data.loc[self.current_time, 'pnl_pct_change'] = self.pnl_pct_change

    ### Update NAV
    self.log_data.loc[self.current_time, 'nav'] = self.log_data.loc[self.current_time, 'bullets'] + self.log_data.loc[self.current_time, 'holding']
