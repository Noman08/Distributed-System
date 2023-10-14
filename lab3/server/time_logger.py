from utility import currrent_time_secs, sleep

class Constants:
    first_entry_time_in_second = 0 
    last_entry_time = 0 

def set_first_entry_time_in_second():
    Constants.first_entry_time_in_second = currrent_time_secs()
    return Constants.first_entry_time_in_second

def set_last_entry_time():
    Constants.last_entry_time = currrent_time_secs()
    return Constants.last_entry_time

def get_time_difference_between_first_and_last_entry():
    return Constants.last_entry_time - Constants.first_entry_time_in_second
