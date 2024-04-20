import numpy as np                      # Array and matrices processing 
import cv2                              # Images pre-processing
import os, sys                          # Library to connect local variables
import time                             # Time Library
import operator                         # Stand for operator assingnment


from string import ascii_uppercase      # Uppercase the text display

import tkinter as tk                    # Custom GUI for Python
from PIL import Image, ImageTk          # Reading and processing images

from hunspell import Hunspell           # Spellchecking Library python
import enchant                          # Binding for spellchecking (Support Lib)

from keras.model import model_from_json #  Stand for transaction the model with application


os.environ['THEANO_FLAGS'] = "device=cuda, assert_no_cpu_op=True"

# Application GUI Python
class Application:
    def __init__(self): 
        self.hs = Hunspell('en_US')
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.current_image2 = None
        self.json_file = open("Models\model_new.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()


        pass