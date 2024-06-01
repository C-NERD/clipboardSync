#!/bin/python
## synchronizes xsel and wl-clipboard system clipboard contents
## takes wl-clipboard as leader
## meant to be runned during wayland sessions
## pol delay of 500ms

import subprocess, logging
from pathlib import PurePath

log_file = PurePath(__file__).parent / "synchronizer.log"
logging.basicConfig(filename = f"{log_file}", filemode = "w", format = "%(levelname)s :: %(message)s", level = logging.NOTSET)
def request_xsel() -> str:
    
    logging.info("reading xsel clipboard")

    process = subprocess.Popen(["xsel", "-b"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    stdout, _ = process.communicate()
    process.wait()
    return stdout.decode()

def request_wl_clipboard() -> str:
    
    logging.info("reading wl_clipboard")

    process = subprocess.Popen(["wl-paste"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    stdout, _ = process.communicate()
    process.wait()
    return stdout.decode()

def set_xsel_clipboard(data : str):
    
    logging.info("write to xsel clipboard")
    
    process1 = subprocess.Popen(["echo", data], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    process2 = subprocess.Popen(["xsel", "-i", "-b"], stdin = process1.stdout)
    process1.stdout.close()
    process2.wait()

def set_wl_clipboard(data : str):
    
    logging.info("write to wl_clipboard")

    process = subprocess.Popen(["wl-copy", data])
    process.wait()

if __name__ == "__main__":

    from time import sleep
    
    old_xsel_data = request_xsel().strip()
    while True:
        
        wl_data = request_wl_clipboard().strip() 
        xsel_data = request_xsel().strip()
        if wl_data != xsel_data:

            if old_xsel_data != xsel_data:

                set_wl_clipboard(xsel_data) ## It means xsel has been updated, so update wl_clipboard

            else:

                set_xsel_clipboard(wl_data) ## It means wl_clipboard has been updated, so update xsel

        sleep(0.5)

