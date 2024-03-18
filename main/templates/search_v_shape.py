def search_v_shape(self):
    close = self.selected_all_new_data.close.values[-1]
    open = self.selected_all_new_data.open.values[-1]
    tr = self.selected_all_new_data.tr.values[-1]
    atr = self.selected_all_new_data.atr.values[-1]

    self.IsVShape = 0
    if self.CountCandleOfVShape >= 3 and self.CountCandleOfVShape <= 8 and close > open:
        self.IsVShape = 1

    if -tr < -atr:
        self.StartCountOfVShape = 1

    if close < open and self.StartCountOfVShape == 1: 
        self.CountCandleOfVShape+=1
    else:
        self.CountCandleOfVShape = 0
        self.StartCountOfVShape = 0

    # print(f"self.StartCountOfVShape: {self.StartCountOfVShape}")
    # print(f"self.CountCandleOfVShape: {self.CountCandleOfVShape}")
    # print(f"self.IsVShape: {self.IsVShape}")
    ### Update
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsVShape'] = self.IsVShape