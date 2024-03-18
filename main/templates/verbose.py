from _libs import np

def verbose(self):
    if self.show_verbose == True:
        current_time = self.log_data.index[-1]
        open = self.log_data.open[-1]
        high = self.log_data.high[-1]
        low = self.log_data.low[-1]
        close = self.log_data.close[-1]
        _pct_change = self.log_data._pct_change[-1]
        status = self.log_data.status[-1]
        bullets = self.log_data.bullets[-1]
        holding = self.log_data.holding[-1]
        nav = self.log_data.nav[-1]

        # print(self.log_data.tail(1))
        print(f"({self.i}) Current time: {current_time}; Status: {status}, Bullets: {bullets}, Holding: {holding}, NAV: {nav}")
        print(f"self.IsBuySignal: {self.IsBuySignal}, self.IsSellSignal: {self.IsSellSignal}")
        print(f"O: {open}, H: {high}, L: {low}, C: {close}, Pct change: {np.round(_pct_change, 4)}")

        # print(self.log_data.tail(1))
        for i in range(len(self.list_n_time_frames)):
            try:
                n_time_frames = self.list_n_time_frames[i]
                time_in_multi_time_frames = self.log_data[f'time_in_multi_time_frames__{n_time_frames}'][-1]
                IsEMACuttingUp = self.log_data[f'IsEMACuttingUp__{n_time_frames}'][-1]
                IsEMACuttingDown = self.log_data[f'IsEMACuttingDown__{n_time_frames}'][-1]
                print(f"(Time in multi-time frames: {time_in_multi_time_frames}) IsEMACuttingUp: {IsEMACuttingUp}, IsEMACuttingDown: {IsEMACuttingDown}")
                selected_data = self.all_new_data_of_multi_time_frames[i].tail(1)
                time = selected_data.index[0]
                # open = selected_data.open[0]
                # high = selected_data.high[0]
                # low = selected_data.low[0]
                # close = selected_data.close[0]
                interface = selected_data.interface[0]
                IsEMACuttingUp = selected_data['IsEMACuttingUp'][0]
                IsEMACuttingDown = selected_data['IsEMACuttingDown'][0]

                print(f"({n_time_frames}s) Time: {time}; Interface: {interface}, IsEMACuttingUp: {IsEMACuttingUp}, IsEMACuttingDown: {IsEMACuttingDown}")
                # print(f"O: {open}, H: {high}, L: {low}, C: {close}")

            except:
                pass

        print()
