#!/usr/bin/python
#-*- coding: utf-8 -*-
import threading
import time
from datetime import datetime

import math
import cv2
import numpy as np

time_cycle = 80

class MyAlgorithm(threading.Thread):

    def __init__(self, camera, motors):
        self.camera = camera
        self.motors = motors
        self.threshold_image = np.zeros((640,360,3), np.uint8)
        self.color_image = np.zeros((640,360,3), np.uint8)
        self.stop_event = threading.Event()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        self.threshold_image_lock = threading.Lock()
        self.color_image_lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)
        self.Kp, self.Kd, self.Ki = 0.0035, 0.004, 0.0001
        self.err, self.vel_err, self.prev_err = 0 ,0, 0
        self.errorList = list()
        self.setpoint = (int(0),int(0))

    def getImage(self):
        self.lock.acquire()
        img = self.camera.getImage().data
        self.lock.release()
        return img

    def set_color_image (self, image):
        img  = np.copy(image)
        if len(img.shape) == 2:
          img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.color_image_lock.acquire()
        self.color_image = img
        self.color_image_lock.release()
        
    def get_color_image (self):
        self.color_image_lock.acquire()
        img = np.copy(self.color_image)
        self.color_image_lock.release()
        return img
        
    def set_threshold_image (self, image):
        img = np.copy(image)
        if len(img.shape) == 2:
          img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        self.threshold_image_lock.acquire()
        self.threshold_image = img
        self.threshold_image_lock.release()
        
    def get_threshold_image (self):
        self.threshold_image_lock.acquire()
        img  = np.copy(self.threshold_image)
        self.threshold_image_lock.release()
        return img

    def run (self):

        while (not self.kill_event.is_set()):
            start_time = datetime.now()
            if not self.stop_event.is_set():
                self.algorithm()
            finish_Time = datetime.now()
            dt = finish_Time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            #print (ms)
            if (ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)

    def stop (self):
        self.stop_event.set()

    def play (self):
        if self.is_alive():
            self.stop_event.clear()
        else:
            self.start()

    def kill (self):
        self.kill_event.set()

    def algorithm(self):
        #GETTING THE IMAGES
        image = self.getImage()
            
        # Add your code here
        reference = (320, 240)
        filtimage = self.process_image(image)
        self.err = self.setpoint[0] - reference[0]
        self.vel_err = self.err - self.prev_err
        self.errorList.append(self.err)
        if(len(self.errorList) > 50):
            self.errorList = self.errorList[-50:]        
        self.errSum = sum(self.errorList)
        self.W = self.err*self.Kp + self.vel_err*self.Kd #+ self.errSum * self.Kd
        self.V = 0 + self.setpoint[1]*6.00/640.00
        self.prev_err = self.errself.setpoint = (int(self.setpoint[0]), int(self.setpoint[1]))
        cv2.circle(filtimage, self.setpoint, 10, (0,255,255), thickness=4, lineType=8, shift=0)
        print "Running"
        print(self.V,self.W)
        #EXAMPLE OF HOW TO SEND INFORMATION TO THE ROBOT ACTUATORS
        
        self.motors.sendV(self.V)
        self.motors.sendW(-self.W)

        #SHOW THE FILTERED IMAGE ON THE GUI
        self.set_threshold_image(filtimage)
        
    def process_image(self, image):
        imageRGB = image
        image = cv2.cvtColor(imageRGB,cv2.COLOR_BGR2RGB)
        lower = np.array([0,0,20], dtype="uint8")
        upper = np.array([7,100,255], dtype="uint8")
        mask0 = cv2.inRange(image, lower, upper)       
        
        begin = 0
        top_point = (500,500)
        bot_point = (-1,-1)
        avg_x , avg_y = -1,-1
        for i in range(300, 420):
            begin = 0
            found = 0
            mx1, mx2, my1, my2 = -1,-1,-1,-1
            for j in range(0, 640):
                if mask0[i,j] > 10 and begin==0:
                    my1, mx1 = i, j
                    begin =1
                if begin == 1 and mask0[i,j] < 10:
                    my2, mx2 = i,j
                    begin = 0
                    found = 1
                    break
            if found == 1:
                avg_x, avg_y = int(mx2+mx1)/2, int(my1+my2)/2
                if (avg_y < top_point[1]):
                    top_point = (avg_x,avg_y)
                if (avg_y > bot_point[1]):
                    bot_point = (avg_x,avg_y)
        if top_point[0] < 500:
            self.setpoint = ((top_point[0]+bot_point[0])/2, (top_point[1]+bot_point[1])/2)            
        cv2.line(image, top_point, bot_point, (0,255,0), 3)        
        self.setpoint = ((top_point[0]+bot_point[0])/2.0, (top_point[1]+bot_point[1])/2.0)
        processed = image
        return image
