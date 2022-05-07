from rtlsdr import RtlSdr
import matplotlib.pyplot as plt
import asyncio
import pandas as pd
from math import sqrt, log
magnitudes = []
async def streaming():
    sdr = RtlSdr()

    # configure device
    sdr.sample_rate = 1e6  # Hz
    sdr.center_freq = 433.875e6     # Hz
    #sdr.freq_correction = 60   # PPM
    sdr.gain = 'auto'


    async for samples in sdr.stream():
        # do something with samples
        # ...
        try:
            print("got samples")
            for sample in samples:
                mag = sqrt(sample.imag ** 2 + sample.real ** 2 )
                mag_db = 20 * log(mag)
                magnitudes.append(mag_db)

            print(len(magnitudes))

        except KeyboardInterrupt:
            pd.DataFrame(magnitudes).to_csv("mag.csv")
            await sdr.stop()
            sdr.close()


print(1)
loop = asyncio.get_event_loop()
loop.run_until_complete(streaming())