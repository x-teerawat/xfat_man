from _libs import *

### Plot
def plot(self):
    ### Colors
    g_03 = "#A2D9CE"
    g_06 = "#16A085"
    g_10 = "#0B5345"

    r_03 = "#F5B7B1"
    r_06 = "#E74C3C"
    r_10 = "#78281F"

    b_03 = "#AED6F1"
    b_06 = "#3498DB"
    orange_06 = "#F39C12"

    purple_06 = "#8E44AD"

    ### Setup
    n_above_percentage = 0.5 # Unit: percentage
    n_below_percentage = 0.5 # Unit: percentage
    below_percentage = 1-(n_above_percentage/100)
    above_percentage = 1+(n_below_percentage/100)
    below_above_percentage = above_percentage*(1-0.0025)
    above_below_percentage = below_percentage*(1+0.0025)

    mc = mpf.make_marketcolors(
        up='green', 
        down='red', 
        edge='black', 
        volume='gray'
    )

    s = mpf.make_mpf_style(
        marketcolors=mc,
        gridcolor='lightgray',
        gridstyle=':',
        # facecolor='#a9a9a9',
        # figcolor='#a9a9a9',
        y_on_right=False
    )

    fig = mpf.figure(style=s, figsize=(7, 4))

    ax1 = fig.add_subplot(8, 1, (1, 4), style=s)
    ax2 = fig.add_subplot(8, 1, (5, 6), style=s, sharex=ax1)
    ax3 = fig.add_subplot(8, 1, (7, 8), style=s, sharex=ax1)
    ax1.tick_params(labelbottom=False)
    ax2.tick_params(labelbottom=False)
    
    plots = [
        ### ax1
        # mpf.make_addplot(self.selected_zig_zag_data['pivot_price'], ax=ax1, color='purple', width=1),
        # mpf.make_addplot(self.selected_zig_zag_data['pivot_ll']*below_percentage, scatter=True, marker="$LL$", markersize=150, ax=ax1, color=g_06),
        # mpf.make_addplot(self.selected_zig_zag_data['pivot_hl']*below_percentage, scatter=True, marker="$HL$", markersize=150, ax=ax1, color=g_06),
        # mpf.make_addplot(self.selected_zig_zag_data['pivot_hh']*above_percentage, scatter=True, marker="$HH$", markersize=150, ax=ax1, color=r_06),
        # mpf.make_addplot(self.selected_zig_zag_data['pivot_lh']*above_percentage, scatter=True, marker="$LH$", markersize=150, ax=ax1, color=r_06),
        # mpf.make_addplot(self.selected_zig_zag_data['pivot_buy_signal']*above_below_percentage, type="scatter", marker="^", markersize=150, ax=ax1, color=g_06),
        # mpf.make_addplot(self.selected_zig_zag_data['pivot_sell_signal']*below_above_percentage, type="scatter", marker="v", markersize=150, ax=ax1, color=r_06),

        ### ax2
        mpf.make_addplot(self.selected_all_new_data[f'ema_{self.n_fast_ema}'].values, ax=ax2, color='blue', width=1),
        mpf.make_addplot(self.selected_all_new_data[f'ema_{self.n_slow_ema}'].values, ylabel=f"EMA{self.n_fast_ema} (B) & EMA{self.n_slow_ema} (R)", ax=ax2, color='red', width=1),

        ### ax3
        mpf.make_addplot([30 for i in range(len(self.selected_all_new_data))], ax=ax3, color='black', linestyle='dotted', width=1),
        mpf.make_addplot([70 for i in range(len(self.selected_all_new_data))], ax=ax3, color='black', linestyle='dotted', width=1),
        mpf.make_addplot(self.selected_all_new_data['rsi'], ax=ax3, color=purple_06, width=1, ylabel="RSI"),
    ]

    ### To determine y lim
    ymin = self.selected_all_new_data['low'].min()*below_percentage*(1-0.003)
    ymax = self.selected_all_new_data['high'].max()*above_percentage*(1+0.003)

    # print(f"ymin: {ymin}")
    # print(f"ymax: {ymax}")

    chart_setup = dict(type='candle', ax=ax1, volume=False)

    mpf.plot(
        self.selected_all_new_data,
        **chart_setup,
        style=s,
        addplot=plots,
        xrotation=7,
        # tight_layout=True,
        tight_layout=False,
        # datetime_format="%d-%b-%y %H:%M:%S",
        datetime_format="%H:%M:%S",
        returnfig=True,
        ylim=(ymin, ymax)
    )
    
    # ### EMA crossover
    # list_date_id_of_ema_crossover = self.selected_all_new_data[self.selected_all_new_data.IsEMACuttingUp==1].date_id.values
    # if len(list_date_id_of_ema_crossover) >= 1:
    #     for ax in [ax1, ax2]:
    #         for x in list_date_id_of_ema_crossover:
    #             ax.axvline(x=x, linestyle='--', color=g_06, alpha=0.75)
    # ### EMA crossunder
    # list_date_id_of_ema_crossunder = self.selected_all_new_data[self.selected_all_new_data.IsEMACuttingDown==1].date_id.values
    # if len(list_date_id_of_ema_crossunder) >= 1:
    #     for ax in [ax1, ax2]:
    #         for x in list_date_id_of_ema_crossunder:
    #             ax.axvline(x=x, linestyle='--', color=r_06, alpha=0.75)

    # ### V shape
    # list_date_id_of_v_shape = self.selected_all_new_data[self.selected_all_new_data.IsVShape==1].date_id.values
    # if len(list_date_id_of_v_shape) >= 1:
    #     for ax in [ax1, ax2]:
    #         for x in list_date_id_of_v_shape:
    #             ax.axvline(x=x, linestyle='--', color=g_06, alpha=0.75)

    # ### Inverse v shape
    # list_date_id_of_inverse_v_shape = self.selected_all_new_data[self.selected_all_new_data.IsInverseVShape==1].date_id.values
    # if len(list_date_id_of_inverse_v_shape) >= 1:
    #     for ax in [ax1, ax2]:
    #         for x in list_date_id_of_inverse_v_shape:
    #             ax.axvline(x=x, linestyle='--', color=r_06, alpha=0.75)

    # ### Turtle shell
    # list_date_id_of_turtle_shell = self.selected_all_new_data[self.selected_all_new_data.IsTurtleShell==1].date_id.values
    # if len(list_date_id_of_turtle_shell) >= 1:
    #     for ax in [ax1, ax2]:
    #         for x in list_date_id_of_turtle_shell:
    #             ax.axvline(x=x, linestyle='--', color=g_06, alpha=0.75)

    # ### Inverse turtle shell
    # list_date_id_of_inverse_turtle_shell = self.selected_all_new_data[self.selected_all_new_data.IsInverseTurtleShell==1].date_id.values
    # if len(list_date_id_of_inverse_turtle_shell) >= 1:
    #     for ax in [ax1, ax2]:
    #         for x in list_date_id_of_inverse_turtle_shell:
    #             ax.axvline(x=x, linestyle='--', color=r_06, alpha=0.75)

    ### Bullish divergence
    list_date_id_of_bullish_divergence = self.selected_all_new_data[self.selected_all_new_data.IsBullishDivergence==1].date_id.values
    if len(list_date_id_of_bullish_divergence) >= 1:
        for ax in [ax1, ax2]:
            for x in list_date_id_of_bullish_divergence:
                ax.axvline(x=x, linestyle='--', color=g_06, alpha=0.75)

    ### Bearish divergence
    list_date_id_of_inverse_bearish_divergence = self.selected_all_new_data[self.selected_all_new_data.IsBearishDivergence==1].date_id.values
    if len(list_date_id_of_inverse_bearish_divergence) >= 1:
        for ax in [ax1, ax2]:
            for x in list_date_id_of_inverse_bearish_divergence:
                ax.axvline(x=x, linestyle='--', color=r_06, alpha=0.75)


    if self.show_plot:
        ### Adjustments to plot
        plt.subplots_adjust(hspace=0)
        mpf.show()

    
    ### Save plot
    if self.save_plot:
        plt.draw()
        plt.savefig(f'{self.folder_name}/{self.round_nth}.png')
        plt.close()
    
    plt.close("all")