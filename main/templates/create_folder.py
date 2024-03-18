from _libs import *

### Create a folder
def create_folder(self):
    if self.save_plot:
        self.folder_name = f"plot__stock_name_{self.stock_name}__buy_strategy_{self.list_buy_strategies}__sell_strategy_{self.list_sell_strategies}__test_date_{self.test_date}__up_thresh_{self.up_thresh}__down_thresh_{self.down_thresh}"
        print(f"self.folder_name: \n{self.folder_name}")
        try:
            os.mkdir(self.folder_name)
        except:
            pass