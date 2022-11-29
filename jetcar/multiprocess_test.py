# !/usr/bin/env python3.6
# coding: utf-8

# Python imports
import time
import threading

# Imports
from Racestick import RaceStick
from nvidia_racecar import NvidiaRacecar
from camera import Camera
# from camera import record_img, dir_check




def autonomous_mode():
    pass


def telemetry_mode():
    global throttle, steering, steeringoffset
    throttle, steering, steeringoffset = controls.GetThrottleSteering()
    car.steering_offset = steeringoffset
    car.RunCar(throttle, steering)


def data_collect_mode(interval):
    
    global cam
    global collectDataState
    
    while True:
        frame, ret = cam.return_frame()
        
        if interval >= 1:
            fname = str(int(time.time()))
            cam.record_data(fname, throttle, steering)
        if interval < 1:
            fname = str(round(time.time(),1)).replace(".","_")
            cam.record_data(fname, throttle, steering)
        cam.save_img_data(frame, fname)
            
        print("I am running {}".format(frame.shape))
        time.sleep(interval)
        
        if collectDataState == False:
            print("Data collection thread stopped")
            break
            

def training_mode():
    pass




if __name__=="__main__":
    
    # Initializing the car
    car = NvidiaRacecar()
    controls = RaceStick()
    cam = Camera()

    throttle = 0.0
    steering = 0.0
    steeringOffset = 0.0
    interval = 0.5
    # dir_check(image_dir_path)

    remoteControl, collectDataState, trainingState, autonomousState, forceStop = controls.GetDriveState()
    prevCollectState = collectDataState
    time.sleep(0.2)
    while not forceStop:
        
        # time.sleep(0.2)
        remoteControl, collectDataState, trainingState, autonomous, forceStop = controls.GetDriveState()
        
        if remoteControl == True:
            telemetry_mode()


        if collectDataState == True and collectDataState != prevCollectState:
            print("collecting data now")
            data_collection_process = threading.Thread(target = data_collect_mode, args=(interval,))
            data_collection_process.start()
            prevCollectState = collectDataState
            
        if collectDataState == False and collectDataState != prevCollectState:
            print("stopping data collection")
            data_collection_process.join()
            prevCollectState = collectDataState
            

        # This will break the loop and stop the program
        if forceStop == True:
            print("Force Stopping")
            break
            
        
            
        
        print(remoteControl, collectDataState, trainingState, autonomous, forceStop, throttle, steering)
        
    print("force stopped")
