
import threading
import time
import atexit
import os
import pyaudio
import numpy as np
import datetime
from gcp_functions import *
from audio_recorder import *
#Script found online to gather PyAudio frames

class MicrophoneRecorder(object):
    def __init__(self, rate=4000, chunksize=1024):
        self.rate = rate
        self.chunksize = chunksize
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunksize,
                                  stream_callback=self.new_frame)
        self.lock = threading.Lock()
        self.stop = False
        self.frames = []
        atexit.register(self.close)

    def new_frame(self, data, frame_count, time_info, status):
        data = np.fromstring(data, 'int16')
        with self.lock:
            self.frames.append(data)
            if self.stop:
                return None, pyaudio.paComplete
        return None, pyaudio.paContinue

    def get_frames(self):
        with self.lock:
            frames = self.frames
            self.frames = []
            return frames
    def start(self):
        self.stream.start_stream()

    def close(self):
        with self.lock:
            self.stop = True
        self.stream.close()
        self.p.terminate()


class LiveSoundAnalysis:
    def __init__(self):
        # init class data
        self.initData()
        
        while 1:
            self.handleNewData()
            time.sleep(0.05)
        


    def initData(self):
        mic = MicrophoneRecorder()
        

        # keeps reference to mic
        self.mic = mic
        self.mic.start()

        # computes the parameters that will be used
        self.freq_vect = np.fft.rfftfreq(mic.chunksize,
                                         1./mic.rate)
        self.time_vect = np.arange(mic.chunksize, dtype=np.float32) / mic.rate * 1000

        
    def handleNewData(self):
        """ handles the asynchroneously collected sound chunks """
        # gets the latest frames
        frames = self.mic.get_frames()

        if len(frames) > 0:
            if frames < 1000:
                frames = 0
            else:
                frames = frames
            current_frame = frames[-1]
            
            
            # computes the fft signal
            fft_frame = np.fft.rfft(current_frame)
            
            fft_frame /= np.abs(fft_frame).max()

            #FFT ANALYSIS

            #CREATES FFT ARRAY
            combined = np.vstack((self.freq_vect, np.abs(fft_frame))).T
            
            #CREATES INPUT SOUND ARRAY
            combined2 = np.vstack((self.time_vect, current_frame)).T
             
            
            for x in combined:
                if x[1] > [0.75] and 1200 < x[0] < 2000:
                    print 'potential siren detected recorded at %s.\n' % (datetime.datetime.now())
                    print 'recording'
                    record_audio()
                    

                    
                    
            
            
            #TEST - returns modal frequency
            #for x in combined:
                #if x[1] == [1.0]:
                   #print x[0]
a = LiveSoundAnalysis()


