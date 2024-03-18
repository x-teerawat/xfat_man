from _libs import *

def force_sell(self):
    if pd.to_datetime(self.current_time.strftime('%H:%M:%S')) >= pd.to_datetime('15:54:59'):
        self.IsBuySignal = 0
        self.IsSellSignal = 1