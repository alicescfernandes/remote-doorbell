from pylab import *
from rtlsdr import *

sdr = RtlSdr()

# configure device
tune_freq = 433.875e6
sdr.sample_rate = 1e6
sdr.center_freq = tune_freq
print(sdr.center_freq / 1e6)
sdr.gain = 10

samples = sdr.read_samples(256*1024)
sdr.close()

# use matplotlib to estimate and plot the PSD
psd_scan, f = psd(samples, NFFT=512, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

for idx, freq in enumerate(f):
    if(freq > (tune_freq / 1e6) - 0.02 and freq < (tune_freq / 1e6) + 0.02 ):
        print(10*np.log10(psd_scan[idx]) )