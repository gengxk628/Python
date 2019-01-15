import tkinter
import time
import math

class Coordinate:  #坐标类，存储游戏中其他类的坐标，并判断相撞与否
    def __init__(self, x, y, width, height):  #此处(x,y)为左上角坐标
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def leftCollide(self, other):  #检测自身左侧是否与other碰撞
        pass

    def rightCollide(self, other):  #检测自身右侧是否与other碰撞
        pass

    def upCollide(self, other):  #检测自身右侧是否与other碰撞
        pass

    def downCollide(self, other):  #检测自身右侧是否与other碰撞
        pass

class Image:
    def __init__(self):
        pass

    def __setConstant(self):  #设置要用到的成员变量
        pass

    def __accessImage(self, fileName):  #读取图片（组）
        pass

    def getImage(self):  #获取当前应该读取的图片
        pass

class StillImage(Image):
    def __init__(self, fileName, x, y, width, height):  #图片名
        self.__setConstant()
        self.__accessImage(fileName)
        self.coordinate=Coordinate(x, y, width, height)
        
    def __setConstant(self):  #设置要用到的成员变量
        self.image=None
        self.coordinate=None
        
    def __accessImage(self, fileName):  #读取图片
        self.image=tkinter.PhotoImage(file=fileName)
        pass

    def getImage(self):  #获取当前应该读取的图片
        return self.image
        pass

class Animation(Image):
    def __init__(self, fileName, x, y, width, height):  #图片名的列表，坐标
        self.__setConstant()
        self.__accessImage(fileName)
        self.coordinate=Coordinate(x, y, width, height)
        
    def __setConstant(self):  #设置要用到的成员变量
        self.image=[]
        self.coordinate=None
        self.on = False  #是否播放动画
        self.index=0  #当前播放动画的帧数
        self.direction="down"

    def __accessImage(self, fileName):  #读取图片组
        for name in fileName:
            self.image.append(tkinter.PhotoImage(file=name))

    def getImage(self):  #获取当前应该读取的图片
        #循环迭代获取图片索引
        if(self.on):
            self.index+=1
            if(self.index >= 5):
                self.index = 0
        else:
            self.index = 0
        #控制返回上下左右的图片
        if(self.direction == "up"):
            return self.image[self.index]
        elif(self.direction == "down"):
            return self.image[self.index + 5]
        elif(self.direction == "left"):
            return self.image[self.index + 10]
        elif(self.direction == "right"):
            return self.image[self.index + 15]
        pass

    def willCollide(self):  #下一步是否将要相撞
        pass

class Map:
    def __init__(self, fileName):
        self.__setConstant()
        self.__accessMap(fileName)

    def __setConstant(self):  #设置一些常量

        #存储游戏地图里的静态物体，10*16，map[15][9]=0代表不存
        self.map = [[0 for i in range(0,10)] for j in range(0,16)]

        #游戏每个格子代表静态物体对应的数字
        self.game_yellowground = 0
        self.game_greenground = 1
        self.game_yellowbox = 2
        self.game_redbox = 3
        self.game_tree = 4
        self.game_house = 5
        #沙地（用0表示，角色可以在上面走）
        #草地（用1表示，角色可以在上面走）
        #黄色的箱子（用2表示，角色可以用炸弹炸掉）
        #绿色的积木（用3表示，角色可以用炸弹炸掉）
        #树（用4表示，不能被炸掉）
        #房子（用5表示，不能被炸掉）
        pass

    def __accessMap(self, fileName):  #加载地图资源
        file = open(fileName)
        for y in range(0,10):
            for x in range(0,16):
                num = int(file.read(1))  #读取每一个格子的信息
                self.map[x][y] = num
                file.read(1)
        file.close()

class Game(Map):
    def __init__(self):
        super().__init__("data/map.txt")

popo=Game()
print(popo.map)
