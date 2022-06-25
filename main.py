
import psutil
import win32process

from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

import win32gui 
import keyboard
import mouse

#not currently used
import os
import time

from combo import Combo

import pythoncom

import threading


SCAN_CODES = {1: 'esc', 2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 
8: '7', 9: '8', 10: '9', 11: '0', 12: '-', 13: '=', 14: 'backspace', 
15: 'tab', 16: 'q', 17: 'w', 18: 'e', 19: 'r', 20: 't', 21: 'y', 22: 'u', 
23: 'i', 24: 'o', 25: 'p', 26: '[', 27: ']', 28: 'enter', 29: 'ctrl', 
30: 'a', 31: 's', 32: 'd', 33: 'f', 34: 'g', 35: 'h', 36: 'j', 37: 'k', 
38: 'l', 39: ';', 40: "'", 41: '`', 42: 'shift', 43: '\\', 44: 'z', 
45: 'x', 46: 'c', 47: 'v', 48: 'b', 49: 'n', 50: 'm', 51: ',', 
52: '.', 53: '/', 54: 'shift', 55: 'print screen', 56: 'alt', 
57: 'space', 58: 'caps lock', 59: 'f1', 60: 'f2', 61: 'f3', 
62: 'f4', 63: 'f5', 64: 'f6', 65: 'f7', 66: 'f8', 67: 'f9', 
68: 'f10', 69: 'num lock', 70: 'scroll lock', 71: 'home', 
72: 'up arrow', 73: 'page up', 74: '-', 75: 'left arrow', 
76: '5', 77: 'right arrow', 78: '+', 79: 'end', 80: 'down arrow', 
81: 'page down', 82: 'insert', 83: 'delete', 87: 'f11', 88: 'f12', 
91: 'windows', 92: 'windows', 93: 'menu'}



class App:
    def __init__(self):
        self.active_keys=set()
        self.combos = [Combo({"end", "mwheelup"}, {"end", "mwheeldown"}, "currentWindow")]
        print(self.combos)
    
    def HandleKeyboard(self, event):
        if event.scan_code in SCAN_CODES:

            key= SCAN_CODES[event.scan_code]

            if event.event_type == "down":
                self.OnPress(key)

            elif event.event_type == "up":
                self.OnRelease(key)

    def HandleMouse(self, event):
        if isinstance(event, mouse._mouse_event.WheelEvent):
            if event.delta < 0 :
                key = "mwheeldown"
            elif event.delta > 0 : 
                key = "mwheelup"
            self.OnPress(key)
            self.OnRelease(key)

        elif isinstance(event, mouse._mouse_event.ButtonEvent):
            key = f"{event.button} mouse button"

            if event.event_type == "down" or event.event_type == "double":
                self.OnPress(key)

            elif event.event_type == "up":
                self.OnRelease(key)

    
    def OnPress(self, key):
        if key not in self.active_keys:
            self.active_keys.add(key)
            for combo in self.combos:
                if combo == self.active_keys:
                    self.HandleAudioChange(combo)
           
            print(self.active_keys)

    def OnRelease(self, key):
        if key in self.active_keys : 
            self.active_keys.remove(key)
            print(self.active_keys)
    
    def GetForegroundProcessName(self):
        pid=win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        p=psutil.Process(pid[-1])
        return p.name()
    
    def HandleAudioChange(self, combo):
        pythoncom.CoInitialize()
        try:
            if combo.combo_type == "currentWindow":
                combo.window_name = self.GetForegroundProcessName()
            
            # if combo.combo_type == "masterVolume":
            #     combo.window_name = 

            volume = combo.GetVolume()
            current_volume = volume.GetMasterVolume()

            if self.active_keys == combo.combo_up:
                if current_volume <=.95:
                    volume.SetMasterVolume(current_volume+.05, None)
                else:
                    volume.SetMasterVolume(1,None)
                    
            elif self.active_keys == combo.combo_down:
                if current_volume >= .05:
                    volume.SetMasterVolume(current_volume-.05, None)
                else:
                    volume.SetMasterVolume(0,None)

            print(current_volume)
            pythoncom.CoUninitialize()

        except:
            print("current window doesn't have volume")
    
    def StartListening(self):
        keyboard.hook_key("end", self.HandleKeyboard, suppress=True)
        keyboard.hook(self.HandleKeyboard)
        mouse.hook(self.HandleMouse)
        print(threading.active_count())
        
        keyboard.wait()


def main():
    app= App()
    app.StartListening()
  
    
    

 
    
if __name__ == "__main__":
    main()


