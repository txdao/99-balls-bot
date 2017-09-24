# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 17:32:35 2017

@author: Tung X. Dao
"""

import pyscreenshot as ImageGrab
import cv2
import numpy as np
import subprocess
import time
import pyautogui

class Game():
    BALL_DIAM_PCT = 0.
    N_BALL_X = 7
    N_BALL_Y = 8
    CIRCLE_Y_PCT = 0.
    CIRCLE_DIAM_PCT = 0.
    LEVEL_NUMBER_X_PCT = 0
    LEVEL_NUMBER_Y_PCT = 0
    STD_BLACK = [0, 0, 0]
    START_BUTTON_PCT = [.50,.60]

    def __init__(self, use_existing_game = False):
        """
        create new instance of game
        determine where the game area is
        """
        # launch browser
        game_url = 'https://www.crazygames.com/assets/99-balls/index.html'
        if use_existing_game:
            print("checking for existing game")
            self.game_coords = self.get_game_coords(self.get_screen_data())
            if self.game_coords is None:
                print("None found, launching new game")
                self.game_coords = self.launch_game_browser(game_url)
                time.sleep(2)
            else:
                print("found existing game")
        else:
            self.launch_game_browser(game_url)
            time.sleep(2)
        self.game_coords = self.get_game_coords(self.get_screen_data())
        self.game_width = self.game_coords[1][0] - self.game_coords[0][0]
        self.game_height = self.game_coords[1][1] - self.game_coords[0][1]
        self.state = []
        self.circle_location = []
        self.level_number = []
        self.ball_locations = []

    def launch_game_browser(self, url):
        """
        launches an instance of the game
        will also move the game window into an appropriate place.
        """

        command = "cmd /c start chrome " + url + " --new-window"
        subprocess.Popen(command,shell=True)

    def get_game_coords(self, img):
        """
        finds the gameplay region
        """
        MIN_MATCH_COUNT = 10
        template = cv2.imread('game_template_small.png')
        img1 = template
        img2 = img

        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1,None)
        kp2, des2 = sift.detectAndCompute(img2,None)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1,des2,k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)

        if len(good)>MIN_MATCH_COUNT:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    #        matchesMask = mask.ravel().tolist()

            h,w,d = img1.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)

            coords = (np.int16(dst[0][0]), np.int16(dst[2][0]))
            return coords

        else:
            print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
            return None

    def start_game(self):
        """
        Presses start
        """
        x = int(self.game_width*self.START_BUTTON_PCT[0] + self.game_coords[0][0])
        y = int(self.game_height*self.START_BUTTON_PCT[1] + self.game_coords[0][1])
        print(x)
        print(y)
        pyautogui.moveTo(x, y)
        pyautogui.click(x=x+1, y=y+1)



    def get_screen_data(self):
        im = ImageGrab.grab()
        im.save('screen_grab.png')
        return cv2.imread('screen_grab.png')


    def reset_game():
        pass

    def get_game_state():
        return None

    def release_circle(angle):
        pass

    def update_game_state():
        pass

    def move_game_area(direction):
        pass


