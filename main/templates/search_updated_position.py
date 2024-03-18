from _libs import *

def search_updated_position(self):
    return np.argwhere(self.n_time_frames==np.array(self.list_n_time_frames))[0][0]