from _libs import *

def search_ema_crossover_and_crosunder(self):
    if len(self.selected_all_new_data) <= 1:
        IsEMACutting = np.nan
        cutting_deg = np.nan
        self.IsEMACuttingUp = np.nan
        self.IsEMACuttingDown = np.nan
        
    else: # len(self.selected_all_new_data) >= 2
        fast_ema_line = self.selected_all_new_data[f"ema_{self.n_fast_ema}"].iloc[-2:].values
        slow_ema_line = self.selected_all_new_data[f"ema_{self.n_slow_ema}"].iloc[-2:].values
        IsEMACutting = np.diff(np.sign(fast_ema_line - slow_ema_line))[0] in [2 , -2] # Cutting up = 2, Cutting down = -2, Not cutting = 0 ### [0] to get a value
        cutting_deg = math.degrees(math.atan(np.diff(fast_ema_line)))

        self.IsEMACuttingUp = 0
        self.IsEMACuttingDown = 0

        if IsEMACutting == True and cutting_deg>0:
            self.IsEMACuttingUp = 1
            self.ema_crossover_time = self.current_time_of_multi_time_frames

            self.cycle_nth += 1

        if IsEMACutting == True and cutting_deg<0:
            self.IsEMACuttingDown = 1
            self.ema_cutting_down_time = self.current_time_of_multi_time_frames

            self.cycle_nth += 1

    ### Update
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsEMACutting'] = IsEMACutting
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'cutting_deg'] = cutting_deg
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsEMACuttingUp'] = self.IsEMACuttingUp
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsEMACuttingDown'] = self.IsEMACuttingDown

    if self.IsEMACuttingUp == 1:
        self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'cutting_up_time'] = self.ema_crossover_time
    if self.IsEMACuttingDown == 1:
        self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'cutting_down_time'] = self.ema_cutting_down_time