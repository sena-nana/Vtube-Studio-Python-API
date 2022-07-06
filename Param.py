from func import *
from setup import *
import time
class DefaultParameters():
    '''
    存储了 VTS 默认参数名称，用于编辑器自动补全
    '''
    FacePositionX:float
    FacePositionY:float
    FacePositionZ:float
    FaceAngleX:float
    FaceAngleY:float
    FaceAngleZ:float
    MouthSmile:float
    MouthOpen:float
    Brows:float
    TongueOut:float
    CheekPuff:float
    FaceAngry:float
    BrowLeftY:float
    BrowRightY:float
    EyeOpenLeft:float
    EyeOpenRight:float
    EyeLeftX:float
    EyeLeftY:float
    EyeRightX:float
    EyeRightY:float
    MousePositionX:float
    MousePositionY:float
    VoiceVolume:float
    VoiceFrequency:float
    VoiceVolumePlusMouthOpen:float
    VoiceFrequencyPlusMouthSmile:float
    MouthX:float
    HandLeftFound:float
    HandRightFound:float
    BothHandsFound:float
    HandDistance:float
    HandLeftPositionX:float
    HandLeftPositionY:float
    HandLeftPositionZ:float
    HandRightPositionX:float
    HandRightPositionY:float
    HandRightPositionZ:float
    HandLeftAngleX:float
    HandLeftAngleZ:float
    HandRightAngleX:float
    HandRightAngleZ:float
    HandLeftOpen:float
    HandRightOpen:float
    HandLeftFinger_1_Thumb:float
    HandLeftFinger_2_Index:float
    HandLeftFinger_3_Middle:float
    HandLeftFinger_4_Ring:float
    HandLeftFinger_5_Pinky:float
    HandRightFinger_1_Thumb:float
    HandRightFinger_2_Index:float
    HandRightFinger_3_Middle:float
    HandRightFinger_4_Ring:float
    HandRightFinger_5_Pinky:float

class Param():
    '''
    与 VTS 通信并存储参数的类，请使用 param 实例化参数调用
    '''
    websocket = None
    async def setup(self):
        '''
        初始化 websocket 信息和插件，并进行一次通信获取参数
        '''
        try:
            self.websocket = await websockets.connect('ws://127.0.0.1:8001')
        except:
            print("Couldn't connect to vtube studio")
            input("press enter to quit program")
            quit()
        await setup(self.websocket)
        await self.update()
    
    async def update(self):
        '''
        更新类中的参数列表，必须在初始化后调用一次才能正常使用获取的参数
        '''
        start=time.time()
        data=await gettrackparam(self.websocket)
        for i in range(20):
            setattr(self,data['data']['defaultParameters'][i]['name'],data['data']['defaultParameters'][i]['value'])
        end=time.time()
        print(f'用时{end-start}')
    
    def paramlist(self):
        '''
        同步函数，获取类中所有参数的值，该函数会返回一个由参数名和值组成的字典
        '''
        data = {}
        for key,value in self.__dict__.items():
            if key != 'websocket':
                data[key]=self.__dict__[key]
        return data

param = Param()

class Buffer():
    '''
    ! 不推荐使用
    VTS 通信过程十分缓慢约 30ms，若用于高帧率要求的应用会产生卡顿
    buffer 能够从两次获取的参数中生成两个中间插值，用于减小卡顿感，但相应的会产生更大的延迟
    buffer 的变量均为列表，格式为 [上一帧，插值帧..，当前帧]
    '''
    async def setup(self):
        '''
        对 buffer 进行初始化，在这个过程中会更新 Param 中的参数值用于生成最初的 buffer 信息
        '''
        self.__dict__ = param.paramlist()
        for key,value in self.__dict__.items():
            self.__dict__[key]=[0,0,0,self.__dict__[key]]
        await self.update()
    async def update(self):
        '''
        对 buffer 参数进行更新，建议与调用参数的方法异步同时使用
        '''
        for key,value in self.__dict__.items():
            self.__dict__[key][0]=self.__dict__[key][2]
        await param.update()
        data = param.paramlist()
        for key,value in self.__dict__.items():
            aframe = (data[key]-self.__dict__[key][0])/3
            self.__dict__[key][1]=(self.__dict__[key][0]+aframe)
            self.__dict__[key][2]=(data[key]-aframe)
            self.__dict__[key][3]=(data[key])
            
#不推荐使用 buffer！经过测试延迟会严重影响使用体验
buffer = Buffer()