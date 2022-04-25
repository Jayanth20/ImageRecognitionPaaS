from picamera import PiCamera
from time import sleep
from subprocess import call
import subprocess
import sys
import os

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('ffmpeg')
install('boto3')
import ffmpeg
import boto3
import _thread
import time
import subprocess
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import threading
# https://stackoverflow.com/questions/10759117/converting-jpg-images-to-png
from PIL import Image

install('requests')
import requests

# Contants
FILE_UPLOAD_API = 'https://alcozbkh4a.execute-api.us-east-1.amazonaws.com/v1/upload'
S3_BUCKET_NAME = 'cse546project2videos'

# Initiate the camera module with pre-defined settings.
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
recordingTimeInsec = 2

# setting sqs
sqs = boto3.client("sqs",
	aws_access_key_id = 'AKIAV2EOFAM6NGERWENN',
    aws_secret_access_key = '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',
    region_name = 'us-east-1')

s3 = boto3.client('s3', aws_access_key_id='AKIAV2EOFAM6NGERWENN',
                      aws_secret_access_key='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')

# queue = sqs.get_queue_by_name(QueueName="outputQueue", region_name="us-east-1")

# make API call for sending images
def uploadImages(location, fileName):
    with open(location, 'rb') as f:
        r = requests.post(FILE_UPLOAD_API, files={'file': f, 'fileName': fileName })
        print(r)

# sendVideos('./face_recognition_docker/hello.png', 'hello.png')

def uploadVideo(local_file, s3_file):
    try:
        s3.upload_file(local_file, S3_BUCKET_NAME, s3_file)
        print("Upload Successful")
    except FileNotFoundError:
        print("The file was not found")
    except:
        print("Credentials not available")


# def monitorSQS():

# this will be excuted as thread for each 0.5 seconds
# def convertAndUploadFrame(file_h264, file_mp4, i):
#     # Record a 5 seconds video.
#     camera.start_recording(file_h264)
#     sleep(0.5)
#     camera.stop_recording()
#     print("Rasp_Pi => Video Recorded! \r\n")
#     # Convert the h264 format to the mp4 format.
#     command = "MP4Box -add " + file_h264 + " " + file_mp4
#     call([command], shell=True)
#     print("\r\nRasp_Pi => Video Converted! \r\n")
#     path = "/home/pi/Desktop/CloudProject/frames/"
#     os.system("ffmpeg -i " + str('/home/pi/Desktop/test'+str(i)+'.mp4') + " -r 1 " + str(path) + "image"+str(i)+"-%3d.jpeg")
#     t1 = threading.Thread(target=getFaceRecognitionResult, name=str(i))
#     t1.start()
#     t1.join()
    
def getFaceRecognitionResult(fileName, i):
    # coverting to mp4 and storing in video
    file_mp4 ="/home/pi/Desktop/CloudProject/videos/" + str(i) + ".mp4"
    file_h264 = "/home/pi/Desktop/CloudProject/" + fileName
    command = "MP4Box -add " + file_h264 + " " + file_mp4
    call([command], shell=True)
    path = "/home/pi/Desktop/CloudProject/frames/"
    # converting
    os.system("ffmpeg -i " + str('/home/pi/Desktop/CloudProject/videos/'+str(i)+'.mp4') + " -r 1 " + str(path) + "image"+ str(i)+ "-%3d.jpeg")
    # uploading mp4 video
    uploadVideo(str('/home/pi/Desktop/CloudProject/videos/'+str(i)+'.mp4'), str(i)+'.mp4')
    # upload image1
    im = Image.open(str(path) + "image"+ str(i)+ "-001.jpeg")
    im.save(str(path) + "image"+ str(i)+ "-001.png")
    uploadImages(str(path) + "image"+ str(i)+ "-001.png", "image"+ str(i)+ "-001.png")
    # upload image2
    im = Image.open(str(path) + "image"+ str(i)+ "-002.jpeg")
    im.save(str(path) + "image"+ str(i)+ "-002.png")
    uploadImages(str(path) + "image"+ str(i)+ "-002.png", "image"+ str(i)+ "-002.png")
    print("Completed : ", i)
    # uploading file

# # Record a video and convert it (MP4).
#for i in range(recordingTimeInsec*2):
#    convertAndUploadFrame('/home/pi/Desktop/CloudProject/videos/test'+str(i)+'.h264', '/home/pi/Desktop/CloudProject/videos/test'+str(i)+'.mp4', i)

threads = []
camera.start_recording('1.h264')
print("recording: ", 1)
sleep(0.5)
camera.stop_recording()
threads.append(threading.Thread(target=lambda: getFaceRecognitionResult(str(1)+".h264", 1), name=str(1)))
threads[-1].start()
for i in range(2, 4):
    camera.start_recording(str(i)+'.h264')
    print("recording: ", i)
    sleep(0.5)
    camera.stop_recording()
    threads.append(threading.Thread(target=lambda: getFaceRecognitionResult(str(i)+".h264", i), name=str(i)))
    threads[-1].start()



# '''
# (ffmpeg
#  .input(input_file_name)
#  .filter('fps', fps=10, round = 'up')
#  .output("%s-%%04d.jpg"%(input_file_name[:-4]), **{'qscale:v': 3})
#  .run())'''


