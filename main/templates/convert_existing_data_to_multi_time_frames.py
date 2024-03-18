from _libs import *
from _funcs import *

def convert_existing_data_to_multi_time_frames(self):
    ### Convert to other time frame data
    for self.n_time_frames in self.list_n_time_frames:
        arr_idx = self.existing_data.index[::self.n_time_frames].values
        arr_open = self.existing_data.open.iloc[::self.n_time_frames].values
        arr_high = self.existing_data.groupby(np.arange(len(self.existing_data))//self.n_time_frames).high.max().values
        arr_low = self.existing_data.groupby(np.arange(len(self.existing_data))//self.n_time_frames).low.min().values
        arr_close = self.existing_data.close.iloc[self.n_time_frames-1::self.n_time_frames].values

        selected_position_nth = search_updated_position(self)
        converted_existing_data_multi_time_frames = pd.DataFrame({
            'open': arr_open,
            'high': arr_high,
            'low': arr_low,
            'close': arr_close
        }, index=arr_idx)
        
        ### Update
        self.existing_data_of_multi_time_frames[selected_position_nth] = converted_existing_data_multi_time_frames