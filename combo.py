from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume



# Contains volume up and volume down combos, window name, and combo_type (currentWindow, masterVolume, setWindow)
class Combo: 
    def __init__(self, combo_up = None, combo_down = None, combo_type = None, window_name = None, suppress = False ):
        self.combo_up = combo_up
        self.combo_down = combo_down
        self.combo_type = combo_type
        self.window_name = window_name
        self.suppress = suppress

    def __eq__(self, other):
        if isinstance(other,set):
            return self.combo_up == other or self.combo_down == other
    
    def GetVolume(self):
        if self.window_name:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                if session.Process and session.Process.name() == self.window_name:
                    return volume
        
