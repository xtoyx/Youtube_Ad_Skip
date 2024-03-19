import win32gui
import pyautogui
import time
pyautogui.FAILSAFE = False

class WindowManager:
    # properties
    target_hwnd=0
    windows_hwnd=[]
    askagain=True
    def __init__(self, target_hwnd,askagain):
        self.target_hwnd = target_hwnd
        self.windows_hwnd = []
        self.askagain=askagain
        
    def is_system_window(self, hwnd):
        class_name = win32gui.GetClassName(hwnd)
        window_title = win32gui.GetWindowText(hwnd)
        return "Progman" in class_name or "Settings" in window_title

    def get_windows_with_icons(self):
        windows_with_icons=[]
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) and not self.is_system_window(hwnd):
                windows_with_icons.append(win32gui.GetWindowText(hwnd))
                self.windows_hwnd.append(hwnd)
            return True
        win32gui.EnumWindows(callback, None)
        return windows_with_icons

    def finish(self):
        pyautogui.keyUp('alt')

    def switchforeground(self, mmm):
        pyautogui.keyDown('alt')
        time.sleep(0.15*mmm)
        for i in range(mmm):
            pyautogui.press('tab')
            time.sleep(0.1)
        time.sleep(0.1)
        self.finish()

    def whereisit(self, num, isitoff):
        whereis = 0
        i = 0
        if isitoff:
            i = 1
        for x in self.windows_hwnd:
            if num == x:
                whereis = i
            i += 1
        return whereis

    def navigate_to_target(self):
        #will go to Youtube Music
        perv_window_txt = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        perv_window_hwnd = win32gui.GetForegroundWindow()
        print(f"current_Window {perv_window_txt}")
        windows_with_icons = self.get_windows_with_icons()
        whereis = self.whereisit(self.target_hwnd, self.askagain)
        self.switchforeground(whereis)
        return perv_window_hwnd
       
    def navigate_back(self,perv_hwnd):
        #get back to perv window    
        self.windows_hwnd = []
        windows_with_icons = self.get_windows_with_icons()
        whereis1 = self.whereisit(perv_hwnd, False)
        self.switchforeground(whereis1)

        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == win32gui.GetWindowText(perv_hwnd):
            print("correct")
