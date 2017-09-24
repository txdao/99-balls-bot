# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 12:57:41 2017

@author: Tung X. Dao
"""
import time
import win32api, win32con
import pyautogui

def left_click(game_obj=None, location=None):
    """
    Performs left click.

    If given a game object and location (in pct of game width and height),
    a click will be performed there.
    """

    if game_obj ==  None:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    else:
        x = int(game_obj.game_width*location[0] + game_obj.game_coords[0][0])
        y = int(game_obj.game_height*location[1] + game_obj.game_coords[0][1])
        pyautogui.moveTo(x=x, y=y)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def left_down(game_obj=None, location=None):
#    if game_obj ==  None:
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
#    else:
#        x = int(game_obj.game_width*location[0] + game_obj.game_coords[0][0])
#        y = int(game_obj.game_height*location[1] + game_obj.game_coords[0][1])
#        pyautogui.moveTo(x=x, y=y)

def left_up():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)

#def move_to(game_obj, location):
#    x = int(game_obj.game_width*location[0] + game_obj.game_coords[0][0])
#    y = int(game_obj.game_height*location[1] + game_obj.game_coords[0][1])
#    pyautogui.moveTo(x=x, y=y)