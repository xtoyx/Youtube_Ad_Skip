import numpy as np
import win32gui, win32ui, win32con ,win32api
from ctypes import windll
import time
from threading import Thread, Lock
from alt_tab import WindowManager

class WindowCapture:

    # threading properties
    stopped = True
    lock = None
    screenshot = None
    # properties
    namenum= 0
    w = 1920
    h = 1080
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name=None):
        # create a thread lock object
        self.lock = Lock()
        # find the handle for the window we want to capture.
        # if no window name is given, capture the entire screen
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name) 
            self.namenum=self.hwnd
            if not self.hwnd:
                print('Select A window if None type -1')
                def find_windows_with_class_name(class_name):
                    windows_with_class_name = []

                    def enum_windows_callback(hwnd, lParam):
                        if win32gui.GetClassName(hwnd) == class_name:
                            windows_with_class_name.append(hwnd)
                        return True

                    win32gui.EnumWindows(enum_windows_callback, None)

                    return windows_with_class_name
                class_name_to_find = "Chrome_WidgetWin_1"  # Replace with the class name you want to search for
                windows = find_windows_with_class_name(class_name_to_find)
                list1=[]
                for hwnd in windows:
                    window_title = win32gui.GetWindowText(hwnd)
                    list1.append(window_title)
                def display(list1):
                    counter = 0
                    record = {}
                    for tables in list1:
                        counter += 1
                        record[counter] = tables
                        print("%s. %s" % (counter, tables))
                    return record
                def get_list(record):
                    print("\nPick a number:")
                    choose = input()
                    if choose == -1 :
                        return ""
                    choose = int(choose)
                    
                    if choose in record:        
                        print(record[choose])
                        return record[choose]
                record = display(list1)
                window_name= get_list(record)
                self.hwnd = win32gui.FindWindow(None,window_name) 
                self.namenum=self.hwnd
                if (not self.hwnd or window_name == ""):
                    raise Exception('Window not found: {}'.format(window_name))


        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
    
        # Adjust window size based on DPI scaling factor
        dpi_scale = 0.7 # DPI scaling factor
        self.w = int((window_rect[2] - window_rect[0]) / dpi_scale)
        self.h = int((window_rect[3] - window_rect[1]) / dpi_scale)

        # account for the window border and titlebar and cut them off
        border_pixels = 8 * dpi_scale
        titlebar_pixels = 30 * dpi_scale
        self.w = int(self.w - (border_pixels * 2))
        self.h = int(self.h - titlebar_pixels - border_pixels)
        self.cropped_x = int(border_pixels)
        self.cropped_y = int(titlebar_pixels)

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = int(window_rect[0] + self.cropped_x)
        self.offset_y = int(window_rect[1] + self.cropped_y)

    def get_screenshot(self):
        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)

        #switch if black screen try False,True
        self.switchBlackScreen(cDC,dcObj,True)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[...,:3]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)
    
    def switchBlackScreen(self,cDC,dcObj,ss):
        if ss:
            result = windll.user32.PrintWindow(self.hwnd, cDC.GetSafeHdc(), 3)
        else:
            cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
    
    def click(self,x, y):
        x=(int)(x)
        y=(int)(y)
        perv_x=0
        perv_y=0
        # wincap.click(1176, 339)
        #(4528 , 722)
        count=0
        for i in win32api.GetCursorPos():
            if count==0 :
                perv_x=i
                count+=1
            else :
                perv_y=i
        window_manager = WindowManager(self.hwnd,False)
        perv_hwnd=window_manager.navigate_to_target()
        win32api.SetCursorPos((x+300, y+250))
        time.sleep(0.5)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        time.sleep(0.5)
        window_manager.navigate_back(perv_hwnd)
        win32api.SetCursorPos((perv_x,perv_y))

    # threading methods
    def start(self):
        self.stopped = False
        t = Thread(target=self.run,daemon=True)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            # get an updated image of the game
            screenshot = self.get_screenshot()
            # lock the thread while updating the results
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()
