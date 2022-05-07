from rtlsdr import RtlSdr
from pylab import psd
from numpy import log10, where
from scipy import fft
import time

NFFT = 512
NOTIFICATIONS_PER_MINUTE = 1
MINUTE_IN_SECONDS = 60# Single minute in millis
start_time = int(time.time())
#tune_freq = 433.973e6
tune_freq = 433.87e6

def evaluate_time():
    current_time = int(time.time())
    if(current_time - start_time > MINUTE_IN_SECONDS):
        return True
    return False


sdr = RtlSdr()

sdr.sample_rate = 2e6  # Hz
sdr.center_freq = tune_freq     # Hz
sdr.gain = 20  

sent_notification = False
prev_max_amp = 0
max_amp = 0;
amp = []

while True:
    samples = sdr.read_samples(NFFT)

    psd_scan = fft.fft(samples)
    
    prev_max_amp = max_amp
    max_amp = max(psd_scan)

    f = fft.fftfreq(len(psd_scan)) +  (tune_freq/1e6)
    idx = where(psd_scan == max_amp)[0]
    frequency = f[idx]
    
    print(max_amp, frequency)

    # TODO: Validate the timestamp of the "amp" and verify with the last available timestamp if a minute has passed. If so, send a notification

    if(max_amp > 10 and prev_max_amp < 10 and frequency > (tune_freq / 1e6) - 0.01 and frequency < (tune_freq / 1e6) + 0.01 ):
        print("rising, Send notification")
        # Send notification
        sent_notification = True
    
