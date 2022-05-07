from rtlsdr import RtlSdr
from pylab import psd
from numpy import log10, where
from scipy import fft
import pandas as pd
import time
from datetime import datetime


NFFT = 512
NOTIFICATIONS_PER_MINUTE = 1
MINUTE_IN_SECONDS = 60# Single minute in millis
start_time = int(time.time())

def evaluate_time():

    current_time = int(time.time())
    print(current_time - start_time, datetime.now())
    if(current_time - start_time > MINUTE_IN_SECONDS):
        return True
    return False

while True:
    if(evaluate_time()):
        start_time = int(time.time())

