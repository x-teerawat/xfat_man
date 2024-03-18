from _libs import *

def check_and_update_missing_times(self):
    try:
        n_missing_times = (self.all_new_data.index[-1]-self.all_new_data.index[-2]).seconds - 1

        if n_missing_times >= 1:
            for m_t in range(n_missing_times):
                missing_time = self.all_new_data.index[-2] + relativedelta(seconds=1)
                missing_data = self.all_new_data.loc[self.all_new_data.index<missing_time].tail(14).mean().to_frame().T
                missing_data.index = [missing_time] # Change index
                self.all_new_data = pd.concat([self.all_new_data, missing_data]) # Update all new data
                self.all_new_data.sort_index(inplace=True)  
    except:
        pass