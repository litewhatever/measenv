#!/usr/bin/env python3

"""
A small script to measure humidity and temperature with DHT22 on Raspberry Pi
"""

import time
import board
import adafruit_dht
import logging
import sys
import os
import json

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa E501
ch.setFormatter(formatter)
logger.addHandler(ch)


# Initial the dht device, with data pin connected to
# Set variables for data file and retry:
dhtDevice = adafruit_dht.DHT22(board.D4)
data_file = os.environ['pi_dht22_data_file']
retry_sleep_cycle = 2
retry_cycles = 5


def main():
    retry_count = 1
    while retry_count < retry_cycles:
        try:
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            data = {'timestamp': timestamp,
                    'temperature': temperature,
                    'humidity': humidity}
            with open(data_file, mode='a') as f:
                json.dump(data, f)
                f.write('\n')
            logger.info('temp: %s, hum: %s',
                        data['temperature'], data['humidity'])
            f.close()
            sys.exit(0)
        except RuntimeError as error:
            logger.error(error.args[0])
            logger.info('retrying in %s seconds', retry_sleep_cycle)
            time.sleep(retry_sleep_cycle)
            retry_count = retry_count + 1
            continue
        except Exception as error:
            # dhtDevice.exit()
            raise error


if __name__ == "__main__":
    main()
