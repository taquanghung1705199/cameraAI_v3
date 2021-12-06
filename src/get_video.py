import subprocess
from threading import Thread
import os 
import datetime
import json

def get_multi_video(today, store_name, name, fps, block_time, close_time, url):
    cam = '{}/{}'.format(today, name)
    try:
        os.mkdir(cam)
    except:
        pass
    name = os.path.join(cam, name)
    while True:
        subprocess.run(['ffmpeg',
                        '-stimeout', '3000',
                        '-loglevel', 'quiet',
                        '-rtsp_transport', 'tcp',
                        '-i', '{}'.format(url), 
                        '-c:v', 'copy',
                        '-c:a', 'copy',
                        '-map', '0',
                        '-reset_timestamps', '1',
                        '-f', 'segment',
                        '-segment_time', '{}'.format(block_time),
                        '-segment_format', 'mp4',
                        '-strftime', '1',
                        '{}*%Y-%m-%d-%H:%M:%S.mp4'.format(name)])
        print("Pending")

today = str(datetime.datetime.now()).split(' ')[0]

with open('config.json', 'r') as json_file:
    threads = {}
    config = json.load(json_file)
    cameras = config['cameras']
    block_time = config['block_time']
    store_name = config['store_name']
    close_time = config['close_time']
    try:
        os.mkdir(today)
        # os.mkdir(os.path.join(today, store_name))
    except:
        pass
    for index, camera in enumerate(cameras):
        threads[index] = Thread(target=get_multi_video, args=(today, store_name, camera['name'], 12, block_time, close_time, camera['rtsp']))
    for thread in threads.values():
        thread.start()
    for thread in threads.values():
        thread.join()
