import serial
import pygame
from pygame.locals import *
from detect_note_refactored import NoteDetect



class Send(object):

    def __init__(self):
        print('started init of "Send"')
        pygame.init()
        pygame.display.set_mode((250, 250))
        #mac
        #self.ser = serial.Serial("/dev/tty.usbmodem1421", 115200, timeout=1)
        #linux option 1
        self.ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
        # NOTE: may need to run once at start
        #
        # sudo chmod a+rw /dev/ttyACM0
        #
        #linux option 2
        #self.ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
        self.send_inst = True
        self.note_detector = NoteDetect()
        self.keymap = dict(zip('C C# D D# E F F# G G# A A# B'.split(),range(1,13)))
        print('Press <space> to record note. press <x> to exit')
        self.check_input()

    def check_input(self):
        while self.send_inst:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # execute recording
                        self.note_detector.record()
                        prediction, certainty = self.note_detector.predict()
                        print(f'Note is {prediction} with {certainty}% certainty')
                        signal = self.keymap[prediction]
                        self.ser.write(chr(signal).encode())
                    # exit
                    elif event.key == pygame.K_x:
                        print("Exiting")
                        self.send_inst = False
                        self.ser.write(chr(0).encode())
                        self.ser.close()
                        break


if __name__ == '__main__':
    Send()
