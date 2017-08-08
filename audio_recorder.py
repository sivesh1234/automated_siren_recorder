import pyaudio
import wave
import subprocess
import os
import datetime
import time
import threading
from gcp_functions import *
def record_audio():

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 4000
    CHUNK = 1024
    RECORD_SECONDS = 20 # SET HOW MANY SECONDS TO RECORD
    x =(datetime.datetime.now().time())
    x = str(x).replace(":",".")
    WAVE_OUTPUT_FILENAME = '/home/ubuntu/%s.wav'%x #should be /home/ubuntu/%s.wav on sensor
    print x
 
    audio = pyaudio.PyAudio()
 
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
    print "recording..."
    frames = []
 
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print "finished recording"
    
 
 
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    # MAY HAVE TO DELETE THIS DATA
    print "saving file"
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    
    # CONVERTS TO MP3
    wav = '/home/ubuntu/%s.wav'%x #should be /home/ubuntu/%s.wav on sensor
    cmd = 'lame --preset insane %s' % wav
    subprocess.call(cmd, shell=True)
    os.remove(wav)
    message1 = 'sound file saved at %s.\n' % (datetime.datetime.now())
    publish_message('atomicity-messages',message1)
