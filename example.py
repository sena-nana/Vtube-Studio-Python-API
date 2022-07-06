import pyautogui
from Param import *
from mode import *
from func import *

async def Vface():
    pyautogui.FAILSAFE = False
    loop = asyncio.get_event_loop()
    controller = asyncio.ensure_future(directmouse())
    updater = asyncio.ensure_future(buffer_updater())
    tasks =[updater,controller]
    await asyncio.wait(tasks)

async def main():
    await param.setup()
    print(param.FacePositionX)
    await Vface()

asyncio.run(main())