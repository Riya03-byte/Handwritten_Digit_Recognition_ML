from tokenize import Number
from numpy import testing
import pygame , sys
from pygame import image
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2
from tensorflow.python.keras.backend import constant
import pygame

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont(None, 30)


WINDOWSIZEX = 640
WINDOWSIZEY = 480


PREDICT = True

BOUNDARYINC = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

IMAGESAVE = False

MODEL = load_model("best_model.h5")

LABELS = {0:"Zero" , 1:"One" , 
          2:"Two" , 3:"Three" , 
          4:"Four" , 5:"Five" , 
          6:"Six" , 7:"Seven" ,
          8:"Eight" , 9:"Nine"}

# Initialize Pygame
pygame.init()

#FONT= pygame.font.Font('freesansbold.ttf', 18)
DISPLAYSURF = pygame.display.set_mode((WINDOWSIZEX , WINDOWSIZEY))


pygame.display.set_caption('Digit Board')
iswriting = False

number_xcord = []
number_ycord = []

image_cnt = 1

REDICT = True

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEMOTION and iswriting: # type: ignore
            xcord , ycord = event.pos
            pygame.draw.circle(DISPLAYSURF , WHITE , (xcord , ycord), 4 , 0 )

            number_xcord.append(xcord)
            number_ycord.append(ycord)

        if event.type == MOUSEBUTTONDOWN:
            iswriting = True

        if event.type == MOUSEBUTTONUP:
            iswriting = False    
            number_xcord = sorted(number_xcord)
            number_ycord = sorted(number_ycord)

            if len(number_xcord) > 0:
               rect_min_X = max(number_xcord[0] - BOUNDARYINC, 0)
               rect_max_X = min(WINDOWSIZEX, number_xcord[-1] + BOUNDARYINC)
            else:
               rect_min_X = 0
               rect_max_X = WINDOWSIZEX


            if len(number_ycord) > 0:
               rect_min_Y = max(number_ycord[0] - BOUNDARYINC, 0)
               rect_max_Y = min(WINDOWSIZEY, number_ycord[-1] + BOUNDARYINC)
            else:
               rect_min_Y = 0
               rect_max_Y = WINDOWSIZEY

           

            number_xcord = []
            number_ycord = []

            img_arr = np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_X:rect_max_X , rect_min_Y:rect_max_Y].T.astype(np.float32)

            if IMAGESAVE:
                cv2.imwrite("input_image.png")
                image_cnt += 1

            if REDICT :
                image = cv2.resize(img_arr , (28,28))
                image = np.pad(image , (10,10) , 'constant' , constant_values = 0)
                image = cv2.resize(image , (28,28))/255.0

                Label = str(LABELS[np.argmax(MODEL.predict(image.reshape(1,28,28,1)))])



                textSurface = FONT.render(Label , True , RED , WHITE) # type: ignore
                textRectObj = textSurface.get_rect()
                textRectObj.topleft  = (rect_min_X , rect_max_Y - 30)

                DISPLAYSURF.blit(textSurface , textRectObj)

            if event.type == KEYDOWN:  
                if event.unicode == "n":
                    DISPLAYSURF.fill(BLACK) 
        pygame.display.update()                    