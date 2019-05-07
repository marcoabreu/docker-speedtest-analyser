#!/usr/bin/python3

# Script originally provided by AlekseyP
# https://www.reddit.com/r/technology/comments/43fi39/i_set_up_my_raspberry_pi_to_automatically_tweet/
# modifications by roest - https://github.com/roest01

import os
import csv
import datetime
import time
import os


from pyspeedtest import SpeedTest


def run_speedtest():
    print("--- running speedtest ---")
    download_speed_mb = 0
    upload_speed_mb = 0
    ping_ms = 0

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime("%d.%m.%Y %H:%M:%S")
    try:
        nb_runs = int(os.environ['NB_RUNS']) if 'NB_RUNS' in os.environ else 2
        host = os.environ['HOST'] if 'HOST' in os.environ else None
        # 'speedcheck-ham.kabeldeutschland.de'
        print('Running', nb_runs, ' runs against ', host)
        speed_test = SpeedTest(host=host, runs=nb_runs)
        download_speed_mb = int(10 * speed_test.download() / 1024 / 1024) / 10
        print('Download', download_speed_mb, 'MB/s')
        upload_speed_mb = int(10 * speed_test.upload() / 1024 / 1024) / 10
        print('Upload', upload_speed_mb, 'MB/s')
        ping_ms = int(10 * speed_test.ping()) / 10
        print('Ping', ping_ms, 'ms')


    except Exception as e:
        print("Exception")
        print(e)
        download_speed_mb = 0
        upload_speed_mb = 0
        ping_ms = 0

    print(date, download_speed_mb, upload_speed_mb, ping_ms)

    # save the data to file for local network plotting
    filepath = os.path.dirname(os.path.abspath(__file__)) + "/../data/result.csv"
    fileExist = os.path.isfile(filepath)

    with open(filepath, "a") as out_file:
        writer = csv.writer(out_file)

        if fileExist != True:
            out_file.write("timestamp,ping,download,upload")
            out_file.write("\n")

        writer.writerow((ts * 1000, ping_ms, download_speed_mb, upload_speed_mb))

    return


if __name__ == "__main__":
    try:
        print("start speedtest")
        run_speedtest()
        print("speedtest complete")
    except Exception as e:
        print("Exception")
        print(e)
