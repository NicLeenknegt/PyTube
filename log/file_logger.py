import os
from datetime import datetime

def log(log, file_ext:str = "log", file_name:str = None):
    abs_path = os.getcwd() + "/log/log_files/"
    if file_name is None:
        now:datetime = datetime.now() 
        file_name = str(datetime.timestamp(now))
    
    str_log = str(log)

    log_file = open(abs_path + file_name + "." + file_ext, 'w')
    log_file.write(str_log)
    log_file.close()
    
    return log
