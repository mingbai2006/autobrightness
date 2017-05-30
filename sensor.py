import serial # http://pythonhosted.org/pyserial/pyserial_api.html
import time
import re
import adjust

t = serial.Serial('COM6', 9600)

while True:
    try:
        str = t.read_all()
        match = re.search(r'(\d+)\[lx\]\r\n$', str.decode('utf8')) # 从缓冲区中读取时，可能一次读出多行，用正则取最后一个值
        if match:
            lx = int(match.group(1))
            print('env lx: %s' % lx)
            adjust.setMonitor(lx)
    except serial.serialutil.SerialException as e:
        print(e)
        pass;
    time.sleep(4) # 串口的报告频率约为0.15s