from rtlsdr import RtlSdr
from pylab import psd
from numpy import log10, where
from scipy import fft
import pandas as pd
import time


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

#tune_freq = 433.973e6
tune_freq = 433.87e6

sdr = RtlSdr()

# configure device
sdr.sample_rate = 2e6  # Hz
sdr.center_freq = tune_freq     # Hz
#sdr.freq_correction = 60   # PPM
sdr.gain = 20  

sent_notification = False
prev_max_amp = 0
max_amp = 0;
amp = []
while True:
    samples = sdr.read_samples(NFFT)

    # use matplotlib to estimate and plot the PSD
    psd_scan = fft.fft(samples)
    
    prev_max_amp = max_amp
    max_amp = max(psd_scan)

    f = fft.fftfreq(len(psd_scan)) +  (tune_freq/1e6)
    idx = where(psd_scan == max_amp)[0]
    frequency = f[idx]
    
    print(max_amp, frequency)
    #and frequency > (tune_freq / 1e6) - 0.01 and frequency < (tune_freq / 1e6) + 0.01
    if(max_amp > 10 and prev_max_amp < 10 and frequency > (tune_freq / 1e6) - 0.01 and frequency < (tune_freq / 1e6) + 0.01 ):
        print("rising, Send notification")
        # Send notification
        sent_notification = True

while False:
    samples = sdr.read_samples(NFFT)

    # use matplotlib to estimate and plot the PSD
    psd_scan, f = psd(samples, NFFT=NFFT, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
    psd_scan = 10*log10(psd_scan)
    max_amp = max(psd_scan)
    idx = where(psd_scan == max_amp)[0]
    frequency = f[idx]
    if(max_amp > 1 and frequency > (tune_freq / 1e6) - 0.01 and frequency < (tune_freq / 1e6) + 0.01 ):
        print(max_amp)
        print(idx)
        print(frequency)
    
