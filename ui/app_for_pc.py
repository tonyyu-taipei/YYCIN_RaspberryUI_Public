import eel
import sys
import os
import time
import subprocess
# from dht_reader.dht_reader import DHTReader
import uuid
# from gpiozero import Button
# import cv2
# from picamera2 import Picamera2, Preview
# from inference import get_model
# import supervision as sv
# # # import numpy
# # # from tensorflow.keras.preprocessing import image
# # # from tensorflow.keras.models import load_model
# # model_color = load_model('../models/color_detection挑過.h5')
# model_shape = load_model('../models/shape_detection.h5')

import threading

print("注意：此應用程式僅用於PC端，不支援樹莓派端，所有回傳資料皆為假資料。")

port = 8000
fakeButton = False
stop_thread = False  # 用於控制線程停止的標誌
@eel.expose
def detectButtonPressed():
    # if user enters 1 in command line, return true
    # if user enters 0 in command line, return false
    # if user enters any other value, return true
    return fakeButton
@eel.expose
def readTemp():
    print("讀取溫濕度")
    returnVal = {
        "humidity":60.0,
        "temperature_c":25.5 
    }
    return returnVal
        

@eel.expose
def get_id():
    return os.getenv('SMARTBOX_ID', '').strip() or None



medBoxResult = {
    '1':{'color': "黃色", 'shape': "橢圓形",'amount':2},
    '2':{'color': None, 'shape': None, 'amount':0},
    '3':{'color': None, 'shape': None, 'amount':0},
    '4':{'color': "白色", 'shape': "心形", 'amount':4},
    '5':{'color': None, 'shape': None, 'amount':0},
    '6':{'color': "粉色", 'shape': "圓形", 'amount':3},
    '7':{'color': None, 'shape': None, 'amount':0},
    '8':{'color': None, 'shape': None, 'amount':0},
    
}
@eel.expose
def identification():
    global medBoxResult
    print("模擬識別藥盒中...")
    time.sleep(5)
    try:
        eel.captureHandler()
    except Exception as e:
        print(str(e))
    time.sleep(5)
    print("識別藥盒結果已輸出")
    print(medBoxResult)
    #clear terminal console
    os.system('cls' if os.name == 'nt' else 'clear')

    return medBoxResult

print("藥盒識別碼為：")
print(get_id())

def start_eel():
    #time.sleep(5)  # 等待線程啟動
    eel.start("index.html", size=(960, 540), mode='default', block=False, port=port)
    while not stop_thread:
        eel.sleep(1)  # 使用 eel.sleep 來避免阻塞
    
if __name__ == '__main__':
    eel.init("web")  # 設置根目錄
    t = threading.Thread(target=start_eel)
    t.start()
    # listen for command line input to change fakeButton value
    while True:
        try:
            print("藥盒容器開關模擬：")
            userInput = input("請輸入1(開)或0(關)：")
            if userInput == "0":
                fakeButton = True
            elif userInput == "1":
                fakeButton = False
            elif userInput == "2":
                # restart eel
                stop_thread = True  # 設置標誌來停止線程
                t.join()  # 等待線程終止
                stop_thread = False  # 重置標誌

                t = threading.Thread(target=start_eel)
                # cd to web-src and run npm run build
                os.system("cd web-src && npm run build")
                # 使用 os.execv 來重新啟動程式
                os.system('cls' if os.name == 'nt' else 'clear')
                os.execv(sys.executable, ['python'] + sys.argv)


            else:
                break
        except KeyboardInterrupt:
            break
        except:
            print("Invalid input. Please try again.")
            continue
        time.sleep(1)
