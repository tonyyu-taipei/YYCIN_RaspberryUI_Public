from picamera2 import Picamera2, Preview
import cv2
import time


pic = Picamera2(0)

preconfig = pic.create_preview_configuration(main={"size":(1920,1080)})
pic.configure(preconfig)
pic.start_preview(Preview.QTGL)
pic.set_controls({"ScalerCrop":(0,0,4608,2592)})
pic.start()
pic.set_controls({"AfMode":0,"LensPosition":10, 'AwbEnable':False})
# time.sleep(990)



time.sleep(5)

array= pic.capture_array("main")

cv2.imshow('test',array)
cv2.imwrite("campic.jpg",array)
cv2.waitKey(0)
cv2.destroyWindow('test')