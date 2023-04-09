from keras.models import load_model
import numpy as np
import pygame as pg
import sys
import matplotlib.pyplot as plt
from mypredict import rec_digit

pg.init()
pg.display.set_caption('ЛКМ - Рисовать! ПКМ - Стереть!')
sc = pg.display.set_mode((1200, 800))
panel = pg.Rect(800,0,400,800)
sc.fill((255,255,255))
pg.draw.rect(sc,(181,184,177),panel,0)
pg.display.update()

model = load_model('test_model.h5')

objects = []

font = pg.font.SysFont('Arial', 25)

class MyButton():
    def __init__(self, x, y, width, height, buttonText='Начать', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#a0a0a0',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pg.Surface((self.width, self.height))
        self.buttonRect = pg.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False



    def process(self):
            mousePos = pg.mouse.get_pos()
            self.buttonSurface.fill(self.fillColors['normal'])
            if self.buttonRect.collidepoint(mousePos):
                self.buttonSurface.fill(self.fillColors['hover'])
                if pg.mouse.get_pressed(num_buttons=3)[0]:
                    self.buttonSurface.fill(self.fillColors['pressed'])
                    if self.onePress:
                        self.onclickFunction()
                    elif not self.alreadyPressed:
                        self.onclickFunction()
                        self.alreadyPressed = True
                else:
                    self.alreadyPressed = False
            self.buttonSurface.blit(self.buttonSurf, [
                self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
                self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
            ])
            sc.blit(self.buttonSurface, self.buttonRect)

sc_array =[[0]*800]*800
def predict_and_draw():
    sc_array = np.array(pg.surfarray.array2d(sc))[0:800,:]
    sc_array = np.flip(sc_array,1)
    sc_array = np.rot90(sc_array)

    plt.gray()
    plt.imsave('sc_array.jpg',sc_array)

    pg.draw.rect(sc,(181,184,177),panel,0)

    prediction = rec_digit('sc_array.jpg')

    y_text=50
    for i in range(10):
        sc.blit(font.render(prediction[i],1,(0,0,0)),(820,y_text))
        y_text+=50
    pg.display.update()


customButton = MyButton(800, 700, 400, 100, 'Предсказать', predict_and_draw)
objects.append(customButton)



while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    pressed = pg.mouse.get_pressed()
    pos = pg.mouse.get_pos()
    if pressed[0] and 1<pos[0]<800 and 1<pos[1]<800:
        cr = pg.draw.circle(sc, (30,30,30), pos, 32)
        pg.display.update()
    if pressed[2] and 1<pos[0]<800 and 1<pos[1]<800:
        sc.fill((255,255,255))
        pg.draw.rect(sc,(181,184,177),panel,0)
        pg.display.update()

    for object in objects:
        object.process()
        pg.display.update()
