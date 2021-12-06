#!/usr/bin/env python3
import os
import json
import argparse
from subprocess import Popen


def run(number_process, directory):
    # Popen('python get_video.py', shell=True)
    commands = []
    for r in range(number_process):
        commands.append('python app.py -n {} -r {} -d {}'.format(number_process, r, directory))
    processes = [Popen(cmd, shell=True) for cmd in commands]
    while True:
        for k, p in enumerate(processes):
            if p.poll() is not None:
                print('\n\n******Restarting!******\n\n')
                processes[k] = Popen(commands[k], shell=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-n', '--number_process', metavar='N', type=int, required=True, help='Create number of Thread')
    parser.add_argument('-d', '--directory', metavar='N', type=str, default='/FastMOT/src/data', help='Create Directory')
    para_env = parser.parse_args()
    # with open('config.json', 'r') as json_file:
    #     config = json.load(json_file)
    run(para_env.number_process, para_env.directory)
