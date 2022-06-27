from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume


KEYBOARD_KEYS = ['esc', '1', '2', '3', '4', '5', '6', '7', '8',
    '9', '0', '-', '=', 'backspace', 'tab', 'q', 'w', 'e', 'r', 't',
    'y', 'u', 'i', 'o', 'p', '[', ']', 'enter', 'ctrl', 'a', 's',
    'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", '`', 'shift', 
    '\\', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/',
    'shift', 'print screen', 'alt', 'space', 'caps lock',
    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
    'f10', 'num lock', 'scroll lock', 'home', 'up arrow',
    'page up', '-', 'left arrow', '5', 'right arrow', '+',
    'end', 'down arrow', 'page down', 'insert', 'delete',
    'f11', 'f12', 'windows', 'windows', 'menu']

import keyboard

# Contains volume up and volume down combos, window name, and combo_type (currentWindow, masterVolume, setWindow)
class Combo: 
    def __init__(self, combo_up = None, combo_down = None, combo_type = None, window_name = None, suppress = False, sensitivity= 5 ):
        self._combo_up = combo_up
        self._combo_down = combo_down

        self.combo_type = combo_type
        self.window_name = window_name
        self.suppress = suppress
        self.sensitivity = sensitivity/100

       

    def __eq__(self, other):
        if isinstance(other,set):
            return self._combo_up == other or self._combo_down == other
    
    def SetComboUp(self, new_combo):
        self._combo_up = new_combo
    
    def SetComboDown(self, new_combo):
        self._combo_down = new_combo
    
    def SuppressKeys(self, callback):
        intersection = self._combo_up.intersection(KEYBOARD_KEYS)
        if self.suppress: 
            for key in intersection:
                keyboard.hook_key(key, callback, suppress=True)

    def GetVolume(self):
        if self.window_name:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                if session.Process and session.Process.name() == self.window_name:
                    return volume
        
