# 使用windows monitor API控制显示器参数

from ctypes import windll, byref, Structure, WinError, POINTER, WINFUNCTYPE
from ctypes.wintypes import BOOL, HMONITOR, HDC, RECT, LPARAM, DWORD, BYTE, WCHAR, HANDLE
import math

_MONITORENUMPROC = WINFUNCTYPE(BOOL, HMONITOR, HDC, POINTER(RECT), LPARAM)


class _PHYSICAL_MONITOR(Structure):
    _fields_ = [('handle', HANDLE),
                ('description', WCHAR * 128)]


def _iter_physical_monitors(close_handles=True):
    """Iterates physical monitors.

    The handles are closed automatically whenever the iterator is advanced.
    This means that the iterator should always be fully exhausted!

    If you want to keep handles e.g. because you need to store all of them and
    use them later, set `close_handles` to False and close them manually."""

    def callback(hmonitor, hdc, lprect, lparam):
        monitors.append(HMONITOR(hmonitor))
        return True

    monitors = []
    if not windll.user32.EnumDisplayMonitors(None, None, _MONITORENUMPROC(callback), None):
        raise WinError('EnumDisplayMonitors failed')

    for monitor in monitors:
        # Get physical monitor count
        count = DWORD()
        if not windll.dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(monitor, byref(count)):
            raise WinError()
        # Get physical monitor handles
        physical_array = (_PHYSICAL_MONITOR * count.value)()
        if not windll.dxva2.GetPhysicalMonitorsFromHMONITOR(monitor, count.value, physical_array):
            raise WinError()
        for physical in physical_array:
            yield physical.handle
            if close_handles:
                if not windll.dxva2.DestroyPhysicalMonitor(physical.handle):
                    raise WinError()


def set_vcp_feature(monitor, code, value):
    """Sends a DDC command to the specified monitor.

    See this link for a list of commands:
    ftp://ftp.cis.nctu.edu.tw/pub/csie/Software/X11/private/VeSaSpEcS/VESA_Document_Center_Monitor_Interface/mccsV3.pdf
    """
    if not windll.dxva2.SetVCPFeature(HANDLE(monitor), BYTE(code), DWORD(value)):
        raise WinError()

thresholdLevel = [
    (30, 8, 35), #估计值
    (170, 15, 50),
    (250, 25, 50)
]

BRIGHTNESS = 0x10
CONTRAST=  0x12

currentValue = None

def setBrightness(envLx):
    """输入亮度值，根据阈值设置显示器亮度"""
    global currentValue
    newValue = None
    for k, b, c in thresholdLevel:
        if envLx < k:
            newValue = (b, c)
            break
    if newValue == None:
        last = thresholdLevel[len(thresholdLevel) - 1]
        newValue = (last[1], last[2])

    if currentValue != newValue:
        currentValue = newValue
        for handle in _iter_physical_monitors():
            print('Monitor set: Brightness %s, Contrast %s' % (newValue[0], newValue[1]))
            set_vcp_feature(handle, BRIGHTNESS, newValue[0])
            set_vcp_feature(handle, CONTRAST, newValue[1])

def setMonitor(envLx):
    """输入亮度值，根据阈值设置显示器亮度
    119 => 40
    2 => 2
    bri^b = (envLx+a)
    """
    a = 0
    # b越小，亮度相对越高
    if envLx > 100:
        b = 1.55
        bri = math.pow((envLx + a), (1 / b))
    else:
        b = 1.2
        bri = math.pow((envLx + a), (1 / b))
    bri = math.ceil(bri)
    if envLx < 5:
        contrast = 40
    else:
        contrast = 50
    newValue = (bri, contrast)
    global currentValue
    if currentValue != newValue:
        currentValue = newValue
        for handle in _iter_physical_monitors():
            print('Monitor set: Brightness %s, Contrast %s' % (newValue[0], newValue[1]))
            set_vcp_feature(handle, BRIGHTNESS, newValue[0])
            set_vcp_feature(handle, CONTRAST, newValue[1])
