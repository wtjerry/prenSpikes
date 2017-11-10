import picamera
import time
import sys

video_length = int(sys.argv[1])
t= time.localtime(time.time())
hours = t[3]
minutes = t[4]
seconds = t[5]
file_name = "video_{h}_{m}_{s}.h264".format(h=hours, m=minutes, s=seconds)

camera = picamera.PiCamera()
camera.start_recording(file_name)
time.sleep(video_length)
camera.stop_recording()
