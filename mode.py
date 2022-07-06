import pyautogui
from Param import *
import time
async def click(bool,param,checkpoint):
    if bool==False and param<checkpoint:
        pyautogui.click()
        return True
    if bool==True and param>checkpoint:
        return False
    else:
        return bool

async def keypress(bool,param,checkpoint,key):
    if bool==False and abs(param)>checkpoint:
        pyautogui.keyDown(key)
        print(key,'pressed')
        return True
    if bool==True and abs(param)<checkpoint:
        pyautogui.keyUp(key)
        print(key,'releazed')
        return False
    else:
        return bool

async def directmouse():
    blink = False
    sizex,sizey = pyautogui.size()
    print('directmode')
    frame=0
    while True:
        positionx=sizex/2+param.FaceAngleX*40
        positiony=sizey/2-param.FaceAngleY*80
        blink=await click(blink,param.EyeOpenLeft,0.3)
        pyautogui.moveTo(positionx,positiony)
        await asyncio.sleep(0.01)
        frame += 1
        if frame ==3:
            frame = 0
        print(frame,'contrller update')

async def movemouse():
    pass

async def wasd():
    pass

async def buffer_updater():
    frame=0
    while True:
        await buffer.update()
        print(frame,'updater frame')
        frame += 1