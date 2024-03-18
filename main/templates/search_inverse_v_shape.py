def search_inverse_v_shape(self):
    close = self.selected_all_new_data.close.values[-1]
    open = self.selected_all_new_data.open.values[-1]
    tr = self.selected_all_new_data.tr.values[-1]
    atr = self.selected_all_new_data.atr.values[-1]

    self.IsInverseVShape = 0
    if self.CountCandleOfInverseVShape >= 3 and self.CountCandleOfInverseVShape <= 8 and close < open:
        self.IsInverseVShape = 1

    if tr > atr:
        self.StartCountOfInverseVShape = 1

    if close > open and self.StartCountOfInverseVShape == 1:
        self.CountCandleOfInverseVShape += 1
    else:
        self.StartCountOfInverseVShape = 0
        self.CountCandleOfInverseVShape = 0

    # print(f"self.StartCountOfInverseVShape: {self.StartCountOfInverseVShape}")
    # print(f"self.CountCandleOfInverseVShape: {self.CountCandleOfInverseVShape}")
    # print(f"self.IsInverseVShape: {self.IsInverseVShape}")
    ### Update
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsInverseVShape'] = self.IsInverseVShape