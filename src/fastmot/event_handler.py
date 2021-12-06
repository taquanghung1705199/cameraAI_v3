import ast
import numpy as np
from shapely.geometry import Point, Polygon
import cv2
import json
import datetime

class Handler:

    def __init__(self, main_config):
        self.memory = {}
        self.lines = []
        self.polygons = []
        self.all_events = []
        self.main_config = main_config
        for region in main_config['regions']:
            a_line = {}
            if  region['type'] == 'line':
                points = ast.literal_eval(region['points'])
                a_line['regionID'] = region['regionID']
                a_line['name'] = region['name']
                a_line['type'] = region['type']
                a_line['points'] = [points[0], points[1]]
                a_line['in'] = 0
                a_line['out'] = 0
                self.lines.append(a_line)
            if  region['type'] == 'polygon':
                a_polygon = {}
                points = ast.literal_eval(region['points'])
                a_polygon['regionID'] = region['regionID']
                a_polygon['name'] = region['name']
                a_polygon['type'] = region['type']
                a_polygon['points'] = np.array(points, np.int32)
                a_polygon['contain'] = 0
                a_polygon['in'] = 0
                a_polygon['out'] = 0
                a_polygon['max'] = 0
                self.polygons.append(a_polygon)
    def event(self, regionID, regionName, floor, _type, actionType, timestamp):
        return {
            "regionID": regionID,
            "regionName": regionName,
            "floor": floor,
            "type": _type,
            "actionType": actionType,
            "timestamp": timestamp 
        }

    def get_time_now(self, frame_count, fps, block_start_time):
        second = round(frame_count/fps)
        block_start_time = datetime.datetime.strptime(block_start_time, "%Y-%m-%d %H:%M:%S")
        now = block_start_time + datetime.timedelta(seconds=second)
        return str(now)

    def ccw(self, A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    def intersect(self, A, B, C, D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)

    def detect(self, frame, bboxes, frame_count, fps, block_start_time):
        self.bboxes = bboxes
        boxes = []
        indexIDs = []
        previous = self.memory.copy()
        self.memory = {}
        for key, value in self.bboxes.items():
            boxes.append([value[0], value[1], value[2], value[3]])
            indexIDs.append(int(key))
            self.memory[indexIDs[-1]] = boxes[-1]
        if len(boxes) > 0:
            i = int(0)
            for point_poly in self.polygons:
                if point_poly['contain'] > point_poly['max']:
                    point_poly['max'] = point_poly['contain']
                point_poly['contain'] = 0
            for box in boxes:
                (x,y) = (int(box[0]), int(box[1]))
                (w,h) = (int(box[2]), int(box[3]))
                if indexIDs[i] in previous:
                    previous_box = previous[indexIDs[i]]                                  
                    (x2,y2) = (int(previous_box[0]), int(previous_box[1]))
                    (w2,h2) = (int(previous_box[2]), int(previous_box[3]))
                    p_pre = (int(x2 + (w2-x2)/2), int(y2 + (h2-y2)/2))
                    p_now = (int(x + (w-x)/2), int(y + (h-y)/2))
                    cv2.line(frame, p_now, p_pre, (255,255,255), 3)
                    for point_line in self.lines:
                        if self.intersect(p_now, p_pre, point_line['points'][0], point_line['points'][1]):
                            if self.ccw(p_now, point_line['points'][0], point_line['points'][1])==True and self.ccw(p_pre, point_line['points'][0], point_line['points'][1])==False:
                                point_line['in'] += 1
                                event = self.event(point_line['regionID'], point_line['name'], self.main_config['floor'], point_line['type'], 'in', self.get_time_now(frame_count, fps, block_start_time))
                                self.all_events.append(event)
                            else:
                                point_line['out'] += 1
                                event = self.event(point_line['regionID'], point_line['name'], self.main_config['floor'], point_line['type'], 'out', self.get_time_now(frame_count, fps, block_start_time))
                                self.all_events.append(event)
                    for polygon in self.polygons:
                        poly = Polygon(polygon['points'])
                        point_now = Point(p_now)
                        point_pre = Point(p_pre)
                        if poly.contains(point_now):
                            polygon['contain'] += 1
                        if poly.contains(point_now) and not (poly.contains(point_pre)):
                            polygon['in'] += 1
                            event = self.event(polygon['regionID'], polygon['name'], self.main_config['floor'], polygon['type'], 'in', self.get_time_now(frame_count, fps, block_start_time))
                            self.all_events.append(event)
                        if not (poly.contains(point_now)) and poly.contains(point_pre):
                            polygon['out'] += 1
                            event = self.event(polygon['regionID'], polygon['name'], self.main_config['floor'], polygon['type'], 'out', self.get_time_now(frame_count, fps, block_start_time))
                            self.all_events.append(event)
                i += 1
    
    def draw_line(self, frame):
        for p in self.lines:
                cv2.line(frame, p['points'][0], p['points'][1], (0,255,255), 5)

                cv2.putText(frame, '{}, in: {}/out: {}'.format(p['name'], str(p['in']), str(p['out'])), 
                           p['points'][0], cv2.FONT_HERSHEY_SIMPLEX, 
                            0.5, (255,255,255), 2, cv2.LINE_AA)

    def draw_polygon(self, frame):
        for poly in self.polygons:
                cv2.polylines(frame, [poly['points']], True, (0,255,255), 2)

                cv2.putText(frame, '{}: {}'.format(poly['name'], str(poly['contain'])), 
                           poly['points'][0], cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255,255,255), 2, cv2.LINE_AA)

                cv2.putText(frame, '{}, in: {}/out: {}'.format(poly['name'], str(poly['in']), str(poly['out'])), 
                           poly['points'][1], cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255,255,255), 2, cv2.LINE_AA)

    def output(self, main_config, config2, block_start_time, log):
        text = {}
        text['block_start_time'] = block_start_time
        text['store_name'] = config2['store_name']
        text['cameras'] = []
        a_cam = {}
        a_cam['name'] = main_config['name']
        a_cam['rtsp'] = main_config['rtsp']
        a_cam['events'] = self.all_events
        # text['cameras'].append(a_cam)
        text['cameras'] = a_cam
        if len(a_cam['events']) != 0:
            with open(log, 'w') as out_text:
                json.dump(text, out_text, indent=4)
            