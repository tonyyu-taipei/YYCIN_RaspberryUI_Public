import eel
import os
import sys
import time
from dht_reader.dht_reader import DHTReader
import uuid
from gpiozero import Button
import cv2
from picamera2 import Picamera2, Preview
from inference import get_model
import supervision as sv
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
model_color = load_model('../models/color_detection挑過.h5')
model_shape = load_model('../models/shape_detection.h5')
# 初始化相機
pic = Picamera2(0)
preconfig = pic.create_preview_configuration({ 'size': (4608,2592), 'format':'BGR888'})
pic.configure(preconfig)
pic.set_controls({"ScalerCrop":(0,0,4608,2592)})

pic1 = Picamera2(1)
preconfig1 = pic1.create_preview_configuration({ 'size': (4608,2592), 'format':'BGR888'})
pic1.configure(preconfig1)
pic1.set_controls({"ScalerCrop":(0,0,4608,2592)})

dht_type = "DHT22"
chip_path = "/dev/gpiochip0"
line_offset =3 
sensor_reading_delay = 10.0

identification_lock = False

@eel.expose
def detectButtonPressed():
    try:
        #detect if pin2 is shorted to ground
        button = Button(21)
        pressed = button.is_pressed
        if(pressed):
            print("The medicine box is opened")
        return not pressed
    except Exception as e:
        print(str(e))
        return True

@eel.expose
def readTemp():
    try:
        dht_reader = DHTReader(dht_type, chip_path, line_offset)
        humidity, temperature_c, temperature_f = dht_reader.read_data()
        returnVal = {
            "humidity": humidity,
            "temperature_c": temperature_c
        }
        return returnVal
    except Exception as e:
        print(str(e))
        

@eel.expose
def get_id():
    return os.environ.get("SMARTBOX_ID", "").strip() or None
medImg = {
    '1': None,
    '2': None,
    '3': None,
    '4': None,
    '5': None,
    '6': None,
    '7': None,
    '8': None,
}

medBoxResult = {
    '1':{'color': None, 'shape': None,'amount':0},
    '2':{'color': None, 'shape': None, 'amount':0},
    '3':{'color': None, 'shape': None, 'amount':0},
    '4':{'color': None, 'shape': None, 'amount':0},
    '5':{'color': None, 'shape': None, 'amount':0},
    '6':{'color': None, 'shape': None, 'amount':0},
    '7':{'color': None, 'shape': None, 'amount':0},
    '8':{'color': None, 'shape': None, 'amount':0},
    
}

def yolo_identification(cropped_image):
    if cropped_image is None or cropped_image.size == 0:
        print("Error: cropped_image is empty")
        return []

    api_key = os.environ.get("ROBOFLOW_API_KEY")
    if not api_key:
        raise RuntimeError("ROBOFLOW_API_KEY is required for model inference")
    model_id = os.environ.get("ROBOFLOW_MODEL_ID")
    if not model_id:
        raise RuntimeError("ROBOFLOW_MODEL_ID is required for model inference")
    model = get_model(model_id=model_id, api_key=api_key)
    results = model.infer(cropped_image)
    # return an array of image for different drugs detected
    detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))
    detections.xyxy
    crop = []
    for i, detection in enumerate(detections.xyxy):
        print(detection)
        if detections.confidence[i] >= 0.60:
            # crop the image
            x1, y1, x2, y2 = detection
            width = x2 - x1
            height = y2 - y1
            max_side = max(width, height)
            
            # 計算新的裁切區域，確保為正方形
            new_x1 = max(0, x1 - (max_side - width) // 2)
            new_y1 = max(0, y1 - (max_side - height) // 2)
            new_x2 = min(cropped_image.shape[1], x2 + (max_side - width) // 2)
            new_y2 = min(cropped_image.shape[0], y2 + (max_side - height) // 2)
            
            crop.append(cropped_image[int(new_y1):int(new_y2), int(new_x1):int(new_x2)])

    return crop



def cam_identification(cam_num,pic):
    time.sleep(2)
    array = pic.capture_array("main")

    #cv2.imshow('test{}'.format(cam_num),array)
    #cv2.waitKey(0)
    #cv2.destroyWindow('test{}'.format(cam_num))
    # cv2.imwrite('cam{}.jpg'.format(cam_num),array)
    # print the length of the array
    print(len(array))
    if(cam_num == 0):
        medImg['1'] = array[230:1349, 1123:2184]
        medImg['2'] =  array[67:1306, 2225:3171]
        medImg['5'] = array[1452:2587, 1178:2206]
        medImg['6'] = array[1423:2587, 2239:3324]
    elif(cam_num == 1):
        medImg['3'] = array[209:1255, 1762:2664]
        medImg['4'] = array[0:1240, 3780:2355]
        medImg['7'] = array[1341:2587, 1545:2719]
        medImg['8'] = array[1356:2587, 2782:3948]
    
    # iterate through the dictionary and show the images
def fill_with_average_color(image):
    # 獲取影像的高度和寬度
    h, w, _ = image.shape
    
    # 計算中間區域的範圍（例如，影像中間15%的區域）
    center_h_start = int(h * 0.425)
    center_h_end = int(h * 0.575)
    center_w_start = int(w * 0.425)
    center_w_end = int(w * 0.575)
    
    # 提取中間區域
    center_region = image[center_h_start:center_h_end, center_w_start:center_w_end]
    
    # 計算中間區域的平均顏色
    avg_color = center_region.mean(axis=(0, 1)).astype(int)
    
    # 用平均顏色填滿整個影像
    filled_image = np.full_like(image, avg_color)
    
    return filled_image

def color_identification(cropped_cropped_image_array):
    # convert cropped image to average color
    cropped_cropped_image_array = fill_with_average_color(cropped_cropped_image_array)
    # use tensorflow model to identify the color of the drug
    # load the model
    resized_image = cv2.resize(cropped_cropped_image_array, (300, 300)) 
    # expand the dimensions
    img_array = np.expand_dims(resized_image, axis=0)
    # make the prediction
    prediction = model_color.predict(img_array)
    # get the index of the highest value
    index = np.argmax(prediction)
    # get the color
    color = ['白色', '粉色', '黃色']
    return color[index]

def auto_canny(gray_image):
    # Convert to grayscale
    #gray_image = cv2.cvtColor(gray_image, cv2.COLOR_RGB2GRAY)
    # Ensure the image is in 8-bit unsigned integer format
    gray_image = np.uint8(gray_image)
    # Apply Canny edge detection
    edges = cv2.Canny(gray_image, 100, 200)
    # Expand dimensions to match the expected input shape (64, 64, 1)
    edges = np.expand_dims(edges, axis=-1)
    edges = edges.astype(np.float32)
    return edges

def shape_identification(cropped_cropped_image_array):
    # use tensorflow model to identify the shape of the drug
    # convert cropped image to grey
    cropped_cropped_image_array = cv2.cvtColor(cropped_cropped_image_array, cv2.COLOR_BGR2GRAY)
    # apply canny edge detection
    cropped_cropped_image_array = auto_canny(cropped_cropped_image_array)
    # load the model
    resized_image = cv2.resize(cropped_cropped_image_array, (300, 300)) 
    # expand the dimensions
    img_array = np.expand_dims(resized_image, axis=0)
    # make the prediction
    prediction = model_shape.predict(img_array)
    # get the index of the highest value
    index = np.argmax(prediction)
    # get the shape
    shape = ['圓形', '心形', '橢圓形','膠囊','橢圓形']
    return shape[index]




@eel.expose
def identification():
    medBoxResult = {
    '1':{'color': None, 'shape': None,'amount':0},
    '2':{'color': None, 'shape': None, 'amount':0},
    '3':{'color': None, 'shape': None, 'amount':0},
    '4':{'color': None, 'shape': None, 'amount':0},
    '5':{'color': None, 'shape': None, 'amount':0},
    '6':{'color': None, 'shape': None, 'amount':0},
    '7':{'color': None, 'shape': None, 'amount':0},
    '8':{'color': None, 'shape': None, 'amount':0},
    
    }   

    global identification_lock
    if(identification_lock):
        return False
    pic.start()
    pic1.start()
    pic.set_controls({"AfMode":0,"LensPosition":10, 'AeEnable':False,'AwbEnable':False,"AnalogueGain": 2.0})
    pic1.set_controls({"AfMode":0,"LensPosition":10, 'AeEnable':False,'AwbEnable':False,"AnalogueGain": 2.0})
    time.sleep(3)

    cam_identification(0, pic)
    pic.stop()
    cam_identification(1, pic1)
    pic1.stop()
    try:
        eel.captureHandler()
    except Exception as e:
            print(str(e))
    #preview the image

    for key in medImg:
        if(medImg[key] is not None):
            # cv2.imshow('test{}'.format(key),medImg[key])
            # cv2.waitKey(0)
            # cv2.destroyWindow('test{}'.format(key))
            res = yolo_identification(medImg[key])
            medBoxResult[key]['amount'] = len(res)
            print(len(res))
            color_counter = {}
            shape_counter = {}
            for i in range(len(res)):
                #cv2 show the yolo res
                # cv2.imshow('test{}'.format(i),res[i])
                # cv2.waitKey(0)
                # cv2.destroyWindow('test{}'.format(i))
                color = color_identification(res[i])
                medBoxResult[key]['color'] = color
                print(color)
                shape = shape_identification(res[i])
                medBoxResult[key]['shape'] = shape
                print(shape)
                # 計數顏色
                if color in color_counter:
                    color_counter[color] += 1
                else:
                    color_counter[color] = 1
                
                # 計數形狀
                if shape in shape_counter:
                    shape_counter[shape] += 1
                else:
                    shape_counter[shape] = 1
                most_common_color = max(color_counter, key=color_counter.get)
                most_common_shape = max(shape_counter, key=shape_counter.get)
                
                medBoxResult[key]['color'] = most_common_color
                medBoxResult[key]['shape'] = most_common_shape
    print(medBoxResult)
    identification_lock = False
    return medBoxResult

print("藥盒識別碼為：")
print(get_id())
@eel.expose
def getMedBoxResult():
    return identification()

eel.init("web")
# startup and use kiosk mode
eel.start("index.html", cmdline_args=['--kiosk', '--noerridialogs', '--disable-infobars', '--no-first-run' ,'--ozone-platform=wayland' ,'--enable-features=OverlayScrollbar' ,'--start-maximized'])
