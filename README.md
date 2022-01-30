Use an external light sensor or camera to adjust the brightness of the computer monitor according to the light intensity

---------------------------------------------------------------

使用光传感器或者摄像头来自动调节显示器亮度和对比度

显示器型号：U2515h
### 光传感器 sensor.py
淘宝50元左右，带有USB口，安装驱动后可通过串口读取光强度（lx）数值。已根据当前型号做了标定。

传感器型号：BH1750
### 摄像头 camera.py
零成本，捕捉摄像头画面后使用opencv计算出平均亮度。占用0.3%的CPU，且数值总是有波动，需要做防抖处理。

型号：微软
