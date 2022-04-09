import picamera
from time import sleep
import time
import psutil
INPUT_PATH = "./Input_Videos/video-{}.h264"
cur_status = 0
def video_record(duration):
    cam = picamera.PiCamera()
    cam.start_preview()
    vid_path = INPUT_PATH.format(time.strftime("%Y-%m-%d_%H-%M-%S"))
    cam.start_recording(vid_path, format = "h264")
    cam.wait_recording(duration)
    cam.stop_recording()
    cam.stop_preview()
    cam.close()
    return vid_path

def pi_status():
    if cur_status == "0":
        return False
    return True

def set_busy():
    cur_status = 1
def set_free():
    cur_status = 0
