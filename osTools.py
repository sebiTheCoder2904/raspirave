import os

class OSTool:
    def __init__(self):
        pass    

    # returns the current time in SS MM HH format

    def get_current_time_string(self):
        from time import localtime, strftime
        return strftime("%H:%M:%S", localtime())
