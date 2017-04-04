import cv2
import time
import adjust
# 使用摄像头捕获环境亮度，设置显示器亮度
# 参考资料
# http://blog.topspeedsnail.com/archives/2068
# http://blog.csdn.net/donger_soft/article/details/39522599
# http://docs.opencv.org/3.0-beta/modules/core/doc/operations_on_arrays.html?highlight=avg#CvScalar cvAvg(const CvArr* arr, const CvArr* mask)

cap = cv2.VideoCapture(0)

while (True):
    # 读取一帧
    ret, frame = cap.read()

    # 转为灰度
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 获取亮度
    bri = cv2.mean(gray)[0]
    print('env brightness: %s' % bri)

    # 白天133-170
    adjust.setBrightness(bri)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(10)

# 释放VideoCapture对象
cap.release()