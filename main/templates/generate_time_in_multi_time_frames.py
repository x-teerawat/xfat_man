def generate_time_in_multi_time_frames(all_new_data, n_time_frames, selected_position_nth, round_nth_of_multi_time_frames):
    if len(all_new_data) < n_time_frames:
        time_in_multi_time_frames = all_new_data.index[0]
    elif len(all_new_data)-1 % n_time_frames:
        time_in_multi_time_frames = all_new_data.index[n_time_frames*round_nth_of_multi_time_frames[selected_position_nth]]

    return time_in_multi_time_frames