from picamera import PiCamera
from time import sleep
from subprocess import call 

# Initiate the camera module with pre-defined settings.
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15

def convert(file_h264, file_mp4):
    # Record a 15 seconds video.
    camera.start_recording(file_h264)
    sleep(15)
    camera.stop_recording()
    print("Rasp_Pi => Video Recorded! \r\n")
    # Convert the h264 format to the mp4 format.
    command = "MP4Box -add " + file_h264 + " " + file_mp4
    call([command], shell=True)
    print("\r\nRasp_Pi => Video Converted! \r\n")
    

# Record a video and convert it (MP4).
convert('/home/pi/test.h264', '/home/pi/test.mp4')
