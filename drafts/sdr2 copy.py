from rtlsdr import RtlSdr
from pylab import psd
from numpy import log10, where
import pandas as pd

import asyncio
from math import sqrt, log
magnitudes = []
tune_freq = 433.97e6
NFFT = 1024
async def streaming():
    sdr = RtlSdr()

    # configure device
    sdr.sample_rate = 2e6  # Hz
    sdr.center_freq = tune_freq     # Hz
    #sdr.freq_correction = 60   # PPM
    sdr.gain = 20



    async for samples in sdr.stream():
        try:
                # use matplotlib to estimate and plot the PSD
            psd_scan, f = psd(samples, NFFT=NFFT, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
            psd_scan = 10*log10(psd_scan)
            max_amp = max(psd_scan)
            idx = where(psd_scan == max_amp)[0]
            frequency = f[idx]
            if(max_amp > 1 and frequency > (tune_freq / 1e6) - 0.05 and frequency < (tune_freq / 1e6) + 0.05 ):
                print(max_amp)
                print(idx)
            
        except KeyboardInterrupt:
            print("cenas")
            #pd.DataFrame(magnitudes).to_csv("mag.csv")
            await sdr.stop()
            sdr.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(streaming())