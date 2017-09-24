# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 12:57:41 2017

@author: Tung X. Dao
"""
import time
import win32api, win32con

def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)