def search_turtle_shell(self):
    try:
        front_angle = self.selected_all_new_data.iloc[-3].low_angle
        mid_angle = self.selected_all_new_data.iloc[-2].low_angle
        back_angle = self.selected_all_new_data.iloc[-1].low_angle

        if front_angle < 0 and mid_angle >= 0 and back_angle > 0:
            self.IsTurtleShell = 1
        else:
            self.IsTurtleShell = 0
    except:
        self.IsTurtleShell = 0

    ### Update
    self.selected_all_new_data.loc[self.current_time_of_multi_time_frames, 'IsTurtleShell'] = self.IsTurtleShell