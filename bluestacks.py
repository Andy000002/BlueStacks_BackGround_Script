import win32gui
import win32ui
import win32con
import win32api
import numpy as np
import cv2

class BlueStacks:
    def __init__(self):
        outline_hwnd = win32gui.FindWindow(None, "BlueStacks")
        self.title = win32gui.GetWindowText(outline_hwnd)
        # get control handle
        hwndChilddict = dict()
        win32gui.EnumChildWindows(outline_hwnd, lambda hwnd, param: param.update({win32gui.GetWindowText(hwnd): hwnd}), hwndChilddict)
        self.hwnd = hwndChilddict['BlueStacks Android PluginAndroid']
        self.l, self.t, self.r, self.b = win32gui.GetWindowRect(self.hwnd)
        self.w, self.h = self.r-self.l, self.b-self.t
        # create screenshot
        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
        self.saveDC = self.mfcDC.CreateCompatibleDC()
        self.savebitmap = win32ui.CreateBitmap()
        self.savebitmap.CreateCompatibleBitmap(self.mfcDC, self.w, self.h)

    def Screenshot(self):
        # return ndarray
        self.saveDC.SelectObject(self.savebitmap)
        self.saveDC.BitBlt((0, 0), (self.w, self.h), self.mfcDC, (0, 0), win32con.SRCCOPY)
        signedIntsArray = self.savebitmap.GetBitmapBits(True)
        im_opencv = np.frombuffer(signedIntsArray, dtype="uint8")
        im_opencv.shape = (self.h, self.w, 4)
        cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)
        self.frame = im_opencv
        return self.frame

    def Show_frame(self):
        cv2.imshow(self.title, self.frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def Save_frame(self, name=None):
        if name == None:
            name = self.title
        cv2.imwrite(f"{name}.jpg", self.frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    def Click(self, pos: tuple):
        tmp = win32api.MAKELONG(pos[0], pos[1])
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)

    def Find(self, template):
        # return middle tuple(x, y) of template
        result = cv2.matchTemplate(self.frame[:, :, :-1], template, cv2.TM_SQDIFF_NORMED)
        h, w = template.shape[:2]
        min_val, max_val, min_ind, max_ind = cv2.minMaxLoc(result)
        return (min_ind[0]+w//2, min_ind[1]+h//2)

    def Multi_match(self, template, thres=0.95):
        # return [tuple(middle x, middle y)] of template
        frame = cv2.cvtColor(self.frame[:, :, :-1], cv2.COLOR_BGR2GRAY)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        h, w = template.shape[:2]
        loc = np.where(result >= thres)
        mids = []
        for pt in zip(*loc[::-1]):
            mids.append((pt[0]+w//2, pt[1]+h//2))
        return mids

    def __del__(self):
        win32gui.DeleteObject(self.savebitmap.GetHandle())
        self.saveDC.DeleteDC()
        self.mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwndDC)
