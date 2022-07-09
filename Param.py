from func import *
from setup import *
import time
class DefaultParameters():
    '''
    存储了 VTS 默认参数名称，用于编辑器自动补全
    '''
    FacePositionX:float #脸部位置左右
    FacePositionY:float #脸部位置上下
    FacePositionZ:float #脸部位置远近
    FaceAngleX:float#脸部旋转左右
    FaceAngleY:float#脸部旋转上下
    FaceAngleZ:float#脸部旋转远近（鬼知道什么玩意x
    MouthSmile:float#微笑
    MouthOpen:float#张嘴
    Brows:float       #眉毛
    TongueOut:float#吐舌头
    CheekPuff:float#鼓脸颊
    FaceAngry:float#生气
    BrowLeftY:float#左眉毛上下
    BrowRightY:float#右眉毛上下
    EyeOpenLeft:float#左眼开闭
    EyeOpenRight:float#右眼开闭
    EyeLeftX:float#左眼左右
    EyeLeftY:float#左眼上下
    EyeRightX:float#右眼左右
    EyeRightY:float#右眼上下
    MousePositionX:float#嘴位置左右
    MousePositionY:float#嘴位置上下
    VoiceVolume:float#音量
    VoiceFrequency:float#声音平滑（没试过
    VoiceVolumePlusMouthOpen:float#音量+张嘴
    VoiceFrequencyPlusMouthSmile:float#声音平滑+微笑
    MouthX:float#嘴（不知道什么东西没用过
    HandLeftFound:float#是否找到左手
    HandRightFound:float#是否找到右手
    BothHandsFound:float#是否两个手都找到
    HandDistance:float#两手距离
    HandLeftPositionX:float#左手位置左右
    HandLeftPositionY:float#左手位置上下
    HandLeftPositionZ:float#左手位置远近
    HandRightPositionX:float#右手位置左右
    HandRightPositionY:float#右手位置上下
    HandRightPositionZ:float#右手位置远近
    HandLeftAngleX:float#左手角度左右
    HandLeftAngleZ:float#左手角度上下
    HandRightAngleX:float#右手角度左右
    HandRightAngleZ:float#右手角度上下
    HandLeftOpen:float#左手开闭
    HandRightOpen:float#右手开闭
    HandLeftFinger_1_Thumb:float#左手大拇指弯曲
    HandLeftFinger_2_Index:float#左手食指弯曲
    HandLeftFinger_3_Middle:float#左手中指弯曲
    HandLeftFinger_4_Ring:float#左手无名指弯曲
    HandLeftFinger_5_Pinky:float#左手小拇指弯曲
    HandRightFinger_1_Thumb:float#右手大拇指弯曲
    HandRightFinger_2_Index:float#右手食指弯曲
    HandRightFinger_3_Middle:float#右手中指弯曲
    HandRightFinger_4_Ring:float#右手无名指弯曲
    HandRightFinger_5_Pinky:float#右手小拇指弯曲

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
