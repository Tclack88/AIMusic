import numpy as np
import wave
import struct
import pyaudio
import re

#def find_nearest(array,value):
#    idx = (np.abs(array-value)).argmin()
#    return array[idx]
class NoteDetect():
    def __init__(self):
        self.window_size = 2205    # Size of window to be used for detecting silence
        #self.beta = 1   # Silence detection parameter
        #self.max_notes = 100    # Maximum number of notes in file, for efficiency
        self.sampling_freq = 44100   # Sampling frequency of audio signal
        self.threshold = 600
        
        self.notes = np.array(["C0","C#0","D0","D#0","E0","F0","F#0","G0","G#0","A0","A#0","B0","C1","C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1","A#1","B1","C2","C#2","D2","D#2","E2","F2","F#2","G2","G2#","A2","A2#","B2","C3","C3#","D3","D3#","E3","F3","F3#","G3","G3#","A3","A3#","B3","C4","C4#","D4","D4#","E4","F4","F4#","G4","G4#","A4","A4#","B4","C5","C5#","D5","D5#","E5","F5","F5#","G5","G5#","A5","A5#","B5","C6","C6#","D6","D6#","E6","F6","F6#","G6","G6#","A6","A6#","B6","C7","C7#","D7","D7#","E7","F7","F7#","G7","G7#","A7","A7#","B7","C8","C8#","D8","D8#","E8","F8","F8#","G8","G8#","A8","A8#","B8","Beyond B8"])
        self.frequencies = np.array([16.35,17.32,18.35,19.45,20.60,21.83,23.12,24.50,25.96   ,27.50  ,29.14  ,30.87  ,32.70  ,34.65  ,36.71  ,38.89  ,41.20  ,43.65  ,46.25  ,49.00  ,51.91  ,55.00  ,58.27  ,61.74  ,65.41  ,69.30  ,73.42  ,77.78  ,82.41  ,87.31  ,92.50  ,98.00  ,103.83 ,110.00 ,116.54 ,123.47 ,130.81 ,138.59 ,146.83 ,155.56 ,164.81 ,174.61 ,185.00 ,196.00 ,207.65 ,220.00 ,233.08 ,246.94 ,261.63 ,277.18 ,293.66 ,311.13 ,329.63 ,349.23 ,369.99 ,392.00 ,415.30 ,440.00 ,466.16 ,493.88 ,523.25 ,554.37 ,587.33 ,622.25 ,659.26 ,698.46 ,739.99 ,783.99 ,830.61 ,880.00 ,932.33 ,987.77 ,1046.50    ,1108.73    ,1174.66    ,1244.51    ,1318.51    ,1396.91    ,1479.98    ,1567.98    ,1661.22    ,1760.00    ,1864.66    ,1975.53    ,2093.00    ,2217.46    ,2349.32    ,2489.02    ,2637.02    ,2793.83    ,2959.96    ,3135.96    ,3322.44    ,3520.00    ,3729.31    ,3951.07    ,4186.01    ,4434.92    ,4698.64    ,4978.03    ,5274.04    ,5587.65    ,5919.91    ,6271.93    ,6644.88    ,7040.00    ,7458.62    ,7902.13,8000])
        
    
    def record(self):
        self.Identified_Notes = []
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        fs = 44100  # Record at 44100 samples per second
        seconds = 3
        self.filename = "tempfile.wav"
        
        p = pyaudio.PyAudio()  # Create an interface to PortAudio
        
        print(f'Recording for {seconds} seconds...')
        
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)
        
        frames = []  # Initialize array to store frames
        
        # Store data in chunks for 3 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)
        
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()
        
        print('Finished recording')
        
        # Save the recorded data as a WAV file
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
    
    
    def predict(self):
        ############################## Read Audio File ########################
        print ('\n\nReading Audio File...')
        
        sound_file = wave.open(self.filename, 'r')
        file_length = sound_file.getnframes()
        
        sound = np.zeros(file_length)
        mean_square = []
        sound_square = np.zeros(file_length)
        for i in range(file_length):
            data = sound_file.readframes(1)
            data = struct.unpack("<h", data)
            sound[i] = int(data[0])
            
        sound = np.divide(sound, float(2**15))  # Normalize data in range -1 to 1
        
        
        ###################### DETECTING SCILENCE ##################################
        
        sound_square = np.square(sound)
        frequency = []
        dft = []
        i = 0
        j = 0
        k = 0    
        # traversing sound_square array with a fixed window_size
        while(i<=len(sound_square)-self.window_size):
            s = 0.0
            j = 0
            while(j<=self.window_size):
                s = s + sound_square[i+j]
                j = j + 1   
        # detecting the silence waves
            if s < self.threshold:
                if(i-k>self.window_size*4):
                    dft = np.array(dft) # applying fourier transform function
                    dft = np.fft.fft(sound[k:i])
                    dft=np.argsort(dft)
        
                    if(dft[0]>dft[-1] and dft[1]>dft[-1]):
                        i_max = dft[-1]
                    elif(dft[1]>dft[0] and dft[-1]>dft[0]):
                        i_max = dft[0]
                    else :  
                        i_max = dft[1]
        # claculating frequency             
                    frequency.append((i_max*self.sampling_freq)/(i-k))
                    dft = []
                    k = i+1
            i = i + self.window_size
        
        #print('length',len(frequency))
        #print("frequency")   
        
        for i in frequency :
            #print(i)
            idx = (np.abs(self.frequencies-i)).argmin()
            self.Identified_Notes.append(self.notes[idx])
        
        
        def filter_results(results):
            # Removes C0 ( always present)
            # remove octave letter (eg. D4 -> D)
            C0_removed = [note for note in results if note != 'C0']
            filtered = [re.sub(r"\d+", "", i) for i in C0_removed]
            return filtered
        
        filtered_results = filter_results(self.Identified_Notes)
        
        length = len(filtered_results)
        
        results_weighted = {i:filtered_results.count(i)/length for i in filtered_results}
        likely_answer = max(results_weighted, key=results_weighted.get)
        certainty = results_weighted[likely_answer]*100
        
        #print(f'predict {likely_answer} with {certainty}% certainty')
        return likely_answer, certainty
    
