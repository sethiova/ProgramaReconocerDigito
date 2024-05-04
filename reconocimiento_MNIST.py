import pygame, sys
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2

BOUNDARYINT = 5
WINDOWSIZEX = 640
WINDOWSIZEY = 480

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

IMGSAVE = False
PREDICT = True

MODEL = load_model("bestmodel.keras")

LABELS = {0:"Cero", 1:"Uno",
          2:"Dos", 3:"Tres",
          4:"Cuatro", 5:"Cinco",
          6:"Seis", 7:"Siete",
          8:"Ocho", 9:"Nueve"}

#Inicializar PyGame
pygame.init()

FONT = pygame.font.Font("freesansbold.ttf", 18)
DISPLAYSURF = pygame.display.set_mode((WINDOWSIZEX, WINDOWSIZEY))

pygame.display.set_caption("Canvas de Digito")

iswriting = False

number_xcord = []
number_ycord = []

image_cnt = 1

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION and iswriting:
            xcord, ycord = event.pos
            pygame.draw.circle(DISPLAYSURF, WHITE, (xcord, ycord), 4, 0)
            number_xcord.append(xcord)
            number_ycord.append(ycord)
        if event.type == MOUSEBUTTONDOWN:
            iswriting = True
        if event.type == MOUSEBUTTONUP:
            iswriting = False
            number_xcord = sorted(number_xcord)
            number_ycord = sorted(number_ycord)

            rect_min_x, rect_max_x = max(number_xcord[0]-BOUNDARYINT, 0), min(WINDOWSIZEX, number_xcord[-1]+BOUNDARYINT)
            rect_min_y, rect_max_y = max(number_ycord[0]-BOUNDARYINT, 0), min(number_ycord[-1]+BOUNDARYINT, WINDOWSIZEX)

            number_xcord = []
            number_ycord = []

            img_arr = np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)

            if IMGSAVE:
                cv2.imwrite("image.png")
                image_cnt += 1

            if PREDICT:

                image = cv2.resize(img_arr, (28,28))
                image = np.pad(image, (10,10), 'constant', constant_values = 0)
                image = cv2.resize(image, (28,28)) / 255

                label = str(LABELS[np.argmax(MODEL.predict(image.reshape(1,28,28,1)))])

                textSurface = FONT.render(label, True, RED, WHITE)
                textRecObj = textSurface.get_rect()
                textRecObj.left, textRecObj.bottom = rect_min_x, rect_max_y

                DISPLAYSURF.blit(textSurface, textRecObj)

        if event.type == KEYDOWN:
            if event.unicode == "n":
                DISPLAYSURF.fill(BLACK)

    pygame.display.update()
