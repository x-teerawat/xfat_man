from _libs import *
from _funcs import *

class Utils():
    def run_strategy(self):
        ### Update data
        self.existing_data = pd.concat([self.existing_data, self.new_data])
        self.all_new_data = pd.concat([self.all_new_data, self.new_data])
        self.log_data = pd.concat([self.log_data, self.new_data])

        ### Determine time
        self.current_time = self.log_data.index[-1]
        try:
            self.previous_time = self.log_data.index[-2]
        except:
            pass

        ### Check and update missing times
        check_and_update_missing_times(self)

        ### Buy strategy
        ema_crossover(self)
        v_shape(self)
        turtle_shell(self)
        bullish_divergence(self)

        ### Sell strategy
        ema_crossunder(self)
        inverse_v_shape(self)
        inverse_turtle_shell(self)
        bearish_divergence(self)
        force_sell(self)

        ### Check and update status
        check_and_update_status(self)

        ### Compute NAV
        compute_nav(self)

        ###

        for self.n_time_frames, _list_n_ema in zip(self.list_n_time_frames, self.list_n_ema):
            self.n_fast_ema = _list_n_ema[0]
            self.n_slow_ema = _list_n_ema[1]

            # print(f"self.n_fast_ema: \n{self.n_fast_ema}")
            # print(f"self.n_slow_ema: \n{self.n_slow_ema}")

            self.selected_position_nth = search_updated_position(self)

            if len(self.all_new_data) % self.n_time_frames != 0:
                ### Genterate time in multi time frames
                self.time_in_multi_time_frames = generate_time_in_multi_time_frames(self.all_new_data, self.n_time_frames, self.selected_position_nth, self.round_nth_of_multi_time_frames) # Must be self.time_in_multi_time_frames because update only necessary
                
            else:
                ### Convert 1s time frame to other time frame data
                convert_new_data_to_multi_time_frames(self)

                ### Selected ...
                self.selected_round_nth = self.round_nth_of_multi_time_frames[self.selected_position_nth]
                self.selected_existing_data = self.existing_data_of_multi_time_frames[self.selected_position_nth]
                self.selected_all_new_data = self.all_new_data_of_multi_time_frames[self.selected_position_nth]
                self.current_time_of_multi_time_frames = self.converted_new_data_of_multi_time_frames.index[0]
                try:
                    self.previous_time_of_multi_time_frames = self.selected_all_new_data.index[-2]
                except:
                    pass

                ### EMA indicator
                indicator_ema(self)

                ### RSI indicator
                indicator_rsi(self)

                ### Banker retail indicator
                indicator_banker_retail(self)

                ### TR indicator
                indicator_tr(self)

                ### ATR indicator
                indicator_atr(self)

                ### Zig zag indicator
                indicator_zig_zag(self)

                ### Search AB interfaces
                search_ab_interfaces(self)
                # print(f"self.selected_all_new_data: {self.selected_all_new_data}")
                # print(tabulate(self.selected_all_new_data, self.selected_all_new_data.columns))

                ### Search EMA cutting down
                search_ema_crossover_and_crosunder(self)

                ### Search v shape
                search_v_shape(self)

                ### Search inverse v shape
                search_inverse_v_shape(self)

                ### Compute angle
                compute_angle(self)

                ### Search turtle shell
                search_turtle_shell(self)

                ### Search inverse turtle shell
                search_inverse_turtle_shell(self)

                ### Search bullish divergence
                search_bullish_divergence(self)

                ### Search bearish divergence
                search_bearish_divergence(self)

                ### Compute pivots for plotting
                # self.compute_pivots_for_plotting()
                print(tabulate(self.selected_all_new_data, self.selected_all_new_data.columns))

                ### Plot
                plot(self)

                self.round_nth_of_multi_time_frames[self.selected_position_nth] += 1

            ### Update log_data
            self.log_data.loc[self.current_time, f'time_in_multi_time_frames__{self.n_time_frames}'] = self.time_in_multi_time_frames
            try:
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsEMACuttingUp'] = self.IsEMACuttingUp
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsEMACuttingDown'] = self.IsEMACuttingDown
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsVShape'] = self.IsVShape
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsInverseVShape'] = self.IsInverseVShape
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsTurtleShell'] = self.IsTurtleShell
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsInverseTurtleShell'] = self.IsInverseTurtleShell
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsBullishDivergence'] = self.IsBullishDivergence
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsBearishDivergence'] = self.IsBearishDivergence
            except:
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsEMACuttingUp'] = np.nan
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsEMACuttingDown'] = np.nan
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsTurtleShell'] = np.nan
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsInverseTurtleShell'] = np.nan
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsTurtleShell'] = np.nan
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsInverseTurtleShell'] = np.nan
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsBullishDivergence'] = np.nan
                self.log_data.loc[self.current_time, f'TF{self.n_time_frames}s__IsBearishDivergence'] = np.nan
                

        verbose(self)

        self.round_nth += 1

    