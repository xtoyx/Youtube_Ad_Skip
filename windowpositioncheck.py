import win32gui
import win32api

class WindowPositionChecker:
    def __init__(self):
        pass    
    def get_window_position(self, hwnd):
        monitors = win32api.EnumDisplayMonitors(None, None)
        if len(monitors) == 1:
            first_screen_rect = monitors[0][2]
        elif len(monitors) == 2:
            first_screen_rect = monitors[0][2]
            second_screen_rect = monitors[1][2]

        window_rect = win32gui.GetWindowRect(hwnd)

        window_width = window_rect[2] - window_rect[0]
        window_height = window_rect[3] - window_rect[1]

        # Check if there is only one screen
        if len(monitors) == 1:
            # Check if the window is on the right side of the screen
            if window_rect[0] >= (first_screen_rect[2] - first_screen_rect[0]):
                # Check different positions
                if window_width > 1280 and window_height > 720:
                    return "Full window on first screen", (1100, 807)
                elif window_width > 640 and window_height > 360:
                    return "50% window on first screen", (1808, 610)
                else:
                    return "Window on right side of first screen", (1826, 508)
            else:
                return "Window on left side of first screen", (window_rect[0], window_rect[1])

        # Check if there are two screens
        elif len(monitors) == 2:
            # Check if the window is on the second screen
            if window_rect[0] >= first_screen_rect[2] and window_rect[0] < (second_screen_rect[2] + second_screen_rect[0]):
                # Check different positions
                if window_width > 1280 and window_height > 720:
                    return "Full window on second screen", (2419, 646)
                elif window_width > 640 and window_height > 360:
                    return "50% window on second screen", (4499, 709)
                else:
                    print("Window on right side of second screen")
                    return (3003, 481)

        return "Window position not recognized", None

 #List of poistions One Screen:-
            #the window is in the right side :- x:1826 y:508
            #full window :- x:1100 y:807
            #50% window :- x:1808 y:610
            #Second Screen :-
            #the window is in the right side :- x:4510 y:728
            #full window :- x:3653 y:984
            #50% window :- x:4499 y:709