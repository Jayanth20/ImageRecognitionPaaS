from picamera import PiCamera
from time import sleep
from subprocess import call

import subprocess
import sys

import os


# Initiate the camera module with pre-defined settings.
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15

def convert(file_h264, file_mp4):
    # Record a 5 seconds video.
    camera.start_recording(file_h264)
    sleep(5)
    camera.stop_recording()
    print("Rasp_Pi => Video Recorded! \r\n")
    # Convert the h264 format to the mp4 format.
    command = "MP4Box -add " + file_h264 + " " + file_mp4
    call([command], shell=True)
    print("\r\nRasp_Pi => Video Converted! \r\n")


# Record a video and convert it (MP4).
convert('/home/pi/Desktop/test.h264', '/home/pi/Desktop/test.mp4')

video_file_path = '/home/pi/Desktop/test.mp4'
'''
(ffmpeg
 .input(input_file_name)
 .filter('fps', fps=10, round = 'up')
 .output("%s-%%04d.jpg"%(input_file_name[:-4]), **{'qscale:v': 3})
 .run())'''

path = "/tmp/frames/"
os.system("ffmpeg -i " + str(video_file_path) + " -r 1 " + str(path) + "image-%3d.jpeg")
