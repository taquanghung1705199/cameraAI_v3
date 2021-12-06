#!/usr/bin/env python3
import os
from pathlib import Path
import argparse
import logging
import json
import cv2
import time
import fastmot
from fastmot.utils import ConfigDecoder, Profiler
import datetime
import threading

def main(uri, config, main_config, out, log, mot, gui, verbose, config2, block_start_time):
    args = {}
    args['input_uri'] = uri
    args['config'] = config
    args['log'] = log
    args['output_uri'] = out
    args['mot'] = mot
    args['gui'] = gui
    args['verbose'] = verbose

    # set up logging
    logging.basicConfig(format='%(asctime)s [%(levelname)8s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(fastmot.__name__)
    logger.setLevel(logging.DEBUG if args['verbose'] else logging.INFO)

    # load config file
    with open(args['config']) as cfg_file:
        config = json.load(cfg_file, cls=ConfigDecoder)

    mot = None
    log = None

    stream = fastmot.VideoIO(config['resize_to'], config['video_io'], args['input_uri'], args['output_uri'])

    if args['mot']:
        draw = args['gui'] or args['output_uri'] is not None
        mot = fastmot.MOT(config['resize_to'], config['mot'], main_config, draw=draw, verbose=args['verbose'])
        mot.reset(stream.cap_dt)
        if args['log'] is not None:
            Path(args['log']).parent.mkdir(parents=True, exist_ok=True)
        #     log = open(args['log'], 'w')
    if args['gui']:
        cv2.namedWindow("Video", cv2.WINDOW_AUTOSIZE)

    # logger.info('Starting video capture...')
    stream.start_capture()
    try:
        with Profiler('app') as prof:
            while not args['gui'] or cv2.getWindowProperty("Video", 0) >= 0:
                frame = stream.read()
                if frame is None:
                    break

                if args['mot']:
                    mot.step(frame, stream.cap_fps, block_start_time)

                if args['gui']:
                    cv2.imshow('Video', frame)
                    if cv2.waitKey(1) & 0xFF == 27:
                        break
                if args['output_uri'] is not None:
                    stream.write(frame)
    finally:
        mot.handler.output(main_config, config2, block_start_time, args['log'])
        # clean up resources
        if log is not None:
            log.close()
        stream.release()
        cv2.destroyAllWindows()

    # if args['mot']:
    #     # timing statistics
    #     avg_fps = round(mot.frame_count / prof.duration)
    #     logger.info('Average FPS: %d', avg_fps)
    #     mot.print_timing_info()

def run(directory, config, number_thread, residual):
    while True:
        today = str(datetime.datetime.now()).split(' ')[0]
        store_name = os.path.join(directory, today)
        for cams in os.listdir(today):
            cam = os.path.join(today, cams)
            # if store_name not in cam:
            if int(cam.split('_')[-1]) % number_thread == residual:
                for videos in os.listdir(cam):
                    video = os.path.join(cam, videos)
                    cap = cv2.VideoCapture(video)
                    frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    fps = int(cap.get(cv2.CAP_PROP_FPS))
                    cap.release()
                    if frame == 0 and int(video.split('-')[-2]) < datetime.datetime.now().day:
                        os.remove(video)
                    if frame >= 120:
                        for camera in config['cameras']:
                            if camera['name'] == videos.split('*')[0]:
                                main_config = camera
                                uri = video
                                # print(uri)
                                # config_AI = Path(__file__).parent / 'cfg' / 'mot.json'
                                config_AI = "./cfg/mot.json"
                                # out = '{}/{}_video/{}.mp4'.format(store_name, main_config['name'], videos.split('.')[0])
                                out = None
                                log = '{}/{}_text/{}.json'.format(store_name, main_config['name'], videos.split('.')[0])
                                # print(log)
                                # exit()
                                mot = True
                                gui = False
                                verbose = False
                                block_start_time = videos.split('.')[0].split('*')[-1]
                                block_start_time = str(datetime.datetime.strptime(block_start_time, "%Y-%m-%d-%H:%M:%S"))
                                print("Running {}".format(uri))
                                
                                # main(uri,config_AI,main_config,out,log,mot,gui,verbose, config, block_start_time)
                                # exit()
                                
                                try:
                                    main(uri,config_AI,main_config,out,log,mot,gui,verbose, config, block_start_time)
                                    # new_folder = '{}/{}/{}_out.mp4'.format(store_name, main_config['name'], videos.split('.')[0])
                                    # Path(new_folder).parent.mkdir(parents=True, exist_ok=True)
                                    # os.rename(uri, new_folder)
                                    os.remove(video)
                                except:
                                    os.remove(video)
                    if frame < 120 and frame != 0:
                        os.remove(video)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-n', '--number_thread', metavar='N', type=int, required=True, help='Create number of Thread')
    parser.add_argument('-r', '--residual', metavar='N', type=int, required=True, help='Create Thread')
    parser.add_argument('-d', '--directory', metavar='N', type=str, default='/FastMOT/src/data', help='Create Directory')
    para_env = parser.parse_args()
    number_thread = para_env.number_thread
    residual = para_env.residual
    directory = para_env.directory

    if residual >= number_thread:
        print('residual is less than number of thread !')
        exit()

    with open('config.json', 'r') as json_file:
        config = json.load(json_file)
        run(directory, config, number_thread, residual)