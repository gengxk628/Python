import tkinter
import time
import math

class Coordinate:  #坐标类，存储游戏中其他类的坐标，并判断相撞与否
    def __init__(self, x, y, width, height):  #此处(x,y)为左上角坐标
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def mainIn(self):  #返回角色面积主要存在的元组(用于确定放炸弹的位置)(核心算法之一)

        x=math.floor(self.x)
        y=math.floor(self.y)

        leftupS=(x+1-self.x)*(y+1-self.y)
        leftdownS=(x+1-self.x)*(self.y-y)
        rightdownS=(self.x-x)*(self.y-y)
        rightupS=(self.x-x)*(y+1-self.y)
        if(leftupS>leftdownS and leftupS>rightdownS and leftupS>rightupS):
            return (x,y)
        elif(leftdownS>leftupS and leftdownS>rightdownS and leftdownS>rightupS):
            return (x,y+1)
        elif(rightdownS>leftupS and rightdownS>leftdownS and rightdownS>rightupS):
            return (x+1,y+1)
        elif(rightupS>leftupS and rightupS>leftdownS and rightupS>rightdownS):
            return (x+1,y)

    def collide(self, other):  #检测自身是否与other碰撞，此时类长宽均为1
        if(self.x<other.x+0.69 and self.x+0.69>other.x and self.y<other.y+0.69 and self.y+0.69>other.y):  #两个矩形区域相撞
            return True
        else:
            return False

class MyImage():  #定义一个图像基类
    def __init__(self):
        pass

    def __setConstant(self):  #设置要用到的成员变量
        pass

    def __accessImage(self, fileName):  #读取图片（组）
        pass

    def getImage(self):  #获取当前应该读取的图片
        pass

class StillImage(MyImage,Coordinate):  #游戏中的静态图片
    def __init__(self, fileName, x, y, width, height):  #图片名
        Coordinate.__init__(self,x, y, width, height)
        self.__setStillImageConstant()
        self.__accessImage(fileName)
        
    def __setStillImageConstant(self):  #设置要用到的成员变量
        self.image = None
        pass
        
    def __accessImage(self, fileName):  #读取图片
        self.image = tkinter.PhotoImage(file=fileName)
        pass

    def getImage(self):  #获取当前应该读取的图片
        return self.image
        pass

class Animation(MyImage,Coordinate):  #游戏中的动态图片
    def __init__(self, fileName, x, y, width, height):  #图片名的列表，坐标
        Coordinate.__init__(self,x, y, width, height)
        self.__setAnimationConstant()
        self.__accessImage(fileName)
        
    def __setAnimationConstant(self):  #设置要用到的成员变量
        self.image = []
        self.on = False  #是否播放动画
        self.index = 0  #当前播放动画的帧数
        self.direction = "down"

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

class Role(Animation):  #继承自Animation类
    def __init__(self, fileName, x, y, width, height):
        Animation.__init__(self, fileName, x, y, width, height)
        self.__setRoleConstant()

    def __setRoleConstant(self):
        self.v = 0.08  #角色移动的速度
        pass

    def forward(self):  #根据当前条件前进
        if(self.on):
            if(self.direction == "up"):
                self.y-=self.v
            elif(self.direction == "down"):
                self.y+=self.v
            elif(self.direction == "left"):
                self.x-=self.v
            elif(self.direction == "right"):
                self.x+=self.v
        pass

    def backward(self):  #根据当前条件退后（消除forward）
        if(self.on):
            if(self.direction == "up"):
                self.y+=self.v
            elif(self.direction == "down"):
                self.y-=self.v
            elif(self.direction == "left"):
                self.x+=self.v
            elif(self.direction == "right"):
                self.x-=self.v
        pass

class Bomb(StillImage):
    def __init__(self, fileName, x, y, width, height):  #图片名
        StillImage.__init__(self, fileName, x, y, width, height)

    def __setBombConstant(self):
        self.wholeSpan = 60  #控制炸弹延迟的帧数
        self.currentSpan = 0
        self.on = False  #炸弹是否爆炸

    def next(self):
        self.currentSpan +=1
        if(self.currentSpan>self.wholeSpan):
            self.on = True
            

class Map:
    def __init__(self, fileName):
        self.__setMapConstant()
        self.__accessMap(fileName)

    def __setMapConstant(self):  #设置一些常量

        #存储游戏地图里的静态物体图片，None代表不存
        self.map = [[0 for i in range(0,10)] for j in range(0,16)]
        #存储游戏地图里的静态物体，10*16，map[15][9]=0代表不存
        self.numMap = [[0 for i in range(0,10)] for j in range(0,16)]

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
                self.numMap[x][y] = int(file.read(1))  #读取每一个格子的信息
                if(self.numMap[x][y] == 0 or self.numMap[x][y] == 1):  #num==0 or ==1 说明此处为背景
                    self.map[x][y] = None
                elif(self.numMap[x][y] == 2):
                    self.map[x][y] = StillImage("img/yellowbox.gif",x,y,1,1)
                elif(self.numMap[x][y] == 3):
                    self.map[x][y] = StillImage("img/redbox.gif",x,y,1,1)
                elif(self.numMap[x][y] == 4):
                    self.map[x][y] = StillImage("img/tree.gif",x,y,1,1.5)
                elif(self.numMap[x][y] == 5):
                    self.map[x][y] = StillImage("img/house.gif",x,y,1,1.5)
                file.read(1)
        file.close()

    def willCollide(self, other):  #判断另一个坐标是否会与当前地图中的物体相撞，或者越界（核心算法之一）

        x=math.floor(other.x)
        y=math.floor(other.y)
        if(x<0 or y<0 or x>=15 or y>=9):  #越界(注意四个等号什么时候可以取得，什么时候不能取得，斟酌了好一会)
            return True
        #self.numMap[x][y]>1代表相撞的不是地板
        if(self.numMap[x][y]>1 and self.map[x][y].collide(other) or \
           self.numMap[x+1][y]>1 and self.map[x+1][y].collide(other) or \
           self.numMap[x][y+1]>1 and self.map[x][y+1].collide(other) or \
           self.numMap[x+1][y+1]>1 and self.map[x+1][y+1].collide(other)):  #判断是否相撞
            return True
        return False

class Access:  #读取数据
    def __init__(self):
        self.__setAccessConstant()
        self.__accessImage()
        self.__accessRoles()

    def __setAccessConstant(self):  #要读取的数据
        
        #游戏开始时载入的图片
        self.startphoto = None
        
        #游戏时的背景图
        self.background = None

        #游戏暂停时的图片
        self.pausephoto = None

        #游戏结束时的图片（分别是4位玩家获胜）
        self.endphoto1 = None
        self.endphoto2 = None
        self.endphoto3 = None
        self.endphoto4 = None

        #四个人物的实例
        self.role = []

    def __accessImage(self):  #读取图片的信息
        
        self.startphoto = tkinter.PhotoImage(file="img/startphoto.gif")
        self.background = tkinter.PhotoImage(file="img/background.gif")
        self.pausephoto = tkinter.PhotoImage(file="img/pausephoto.gif")
        self.endphoto1 = tkinter.PhotoImage(file="img/endphoto1.gif")
        self.endphoto2 = tkinter.PhotoImage(file="img/endphoto2.gif")
        self.endphoto3 = tkinter.PhotoImage(file="img/endphoto3.gif")
        self.endphoto4 = tkinter.PhotoImage(file="img/endphoto4.gif")

    def __accessRoles(self):  #读取人物的信息

        namelist = [[],[],[],[]]  #临时存储文件列表名称
        for i in range(0,4):
            for j in range(0,20):
                if(j >= 10):  #j<10的时候要前导0
                    name = "img/role" + str(i) + str(j) + ".gif"
                else:
                    name = "img/role" + str(i) + "0" + str(j) + ".gif"
                namelist[i].append(name)
        self.role.append(Role(namelist[0],15,0,1,1.5))
        self.role.append(Role(namelist[0],0,0,1,1.5))
        self.role.append(Role(namelist[0],0,9,1,1.5))
        self.role.append(Role(namelist[0],15,9,1,1.5))

class Game(Map, Access):  #游戏引擎，继承自Map，Access

    def __init__(self):
        self.__setGameConstant()
        pass
        
    def __setGameConstant(self):  #设置游戏中的一些常量
        #设置游戏的状态参数，根据刷新时根据不同的状态来判定操作
        self.state = 0  #游戏的状态，默认值为game_init

        #游戏的状态参数
        self.game_init = 0  #加载游戏资源
        self.game_start = 1  #选择游戏是否开始（开始界面）
        self.game_run = 2  #游戏进行
        self.game_pause = 3  #游戏暂停
        self.game_end1 = 4   #游戏结束，玩家1胜利
        self.game_end2 = 5   #游戏结束，玩家2胜利
        self.game_end3 = 6   #游戏结束，玩家3胜利
        self.game_end4 = 7   #游戏结束，玩家4胜利

        #显示的宽高
        self.width = 1280
        self.height = 800

        #游戏帧率
        self.fps =30

        #游戏主循环开关
        self.on = False

    def __setScreen(self):  #设置显示模式，以及监听鼠标、键盘按键

        self.popo = tkinter.Tk()
        self.popo.geometry("%dx%d" % (self.width, self.height))  # 设置屏幕的大小
        #self.popo.attributes("-topmost", True) # 显示在最前方
                                                                       #self.popo.overrideredirect(1) # 隐藏标题栏

        self.canvas = tkinter.Canvas(self.popo, width= self.width, height= self.height)
        self.canvas.pack()
        self.canvas.configure(bg="white")
        self.canvas.configure(highlightthickness=0)

        #绑定键盘按键
        self.canvas.bind_all("<KeyPress>", self.__keypress)
        self.canvas.bind_all("<KeyRelease>", self.__keyrelease)

        #绑定鼠标事件
        self.canvas.bind_all("<Button-1>", self.__leftclick)
        self.canvas.bind_all("<Button-3>", self.__rightclick)

    def __mainloop(self):  #游戏开始主循环

        if(self.state == self.game_init):

            self.__setScreen()  #注意此处方法调用的顺序
            Map.__init__(self, "data/map.txt")  #调用父类的构造方法
            Access.__init__(self)

            #初始化之后将状态转化到start
            self.state = self.game_start

        elif(self.state == self.game_start):

            self.canvas.delete("all")
            self.canvas.create_image(640, 400, image = self.startphoto)
            self.canvas.update()

        elif(self.state == self.game_run):

            self.canvas.delete("all")  #很重要，防止canvas重新画出以前的图片，这一条语句调试了很长时间

            self.__moveRoles()
            self.__loadStillImage()
            self.__loadRoles()
            
            self.canvas.update()

        elif(self.state == self.game_pause):

            self.canvas.delete("all")
            self.canvas.create_image(640, 400, image = self.pausephoto)
            self.canvas.update()

        elif(self.state == self.game_end1):
            
            self.canvas.delete("all")
            self.canvas.create_image(640, 400, image = self.endphoto1)
            self.canvas.update()

        elif(self.state == self.game_end2):
            
            self.canvas.delete("all")
            self.canvas.create_image(640, 400, image = self.endphoto2)
            self.canvas.update()

        elif(self.state == self.game_end3):
            
            self.canvas.delete("all")
            self.canvas.create_image(640, 400, image = self.endphoto3)
            self.canvas.update()

        elif(self.state == self.game_end4):
            
            self.canvas.delete("all")
            self.canvas.create_image(640, 400, image = self.endphoto4)
            self.canvas.update()

        pass

    def __moveRoles(self):  #移动角色（并检测碰撞）
        for i in range(0,4):
            self.role[i].forward()
            if(self.willCollide(self.role[i])):
                self.role[i].backward()
        pass

    def __loadStillImage(self):  #画出背景和所有静态图片
        self.canvas.create_image(640, 400, image = self.background)  #画背景
        #画每个格子里的物件
        for i in range(0,16):
            for j in range(0,10):
                if(self.map[i][j] != None):  #map[][]为StillImage对象
                    self.__loadImage(self.map[i][j].getImage(), i,j, self.map[i][j].width, self.map[i][j].height)
                pass

    def __loadRoles(self):  #画人物
        for i in range(0,4):
            self.__loadImage(self.role[i].getImage(), self.role[i].x, self.role[i].y, 1, 1.5)

    def __loadImage(self, photo, x, y, width=1, height=1):
        #加载width*height的静态图片
        #此处的（x,y）表示相对位置（0,0）-（16,10）
        self.canvas.create_image((x + 1 - width / 2) * 80, (y + 1 - height / 2) * 80, image=photo)

    def __keypress(self, event):  #绑定事件
        if(event.keysym == "Return"):  #按下回车键
            self.__continue()
        elif(event.keysym == "Up"):
            self.role[0].direction = "up"
            self.role[0].on = True
        elif(event.keysym == "Down"):
            self.role[0].direction = "down"
            self.role[0].on = True
        elif(event.keysym == "Left"):
            self.role[0].direction = "left"
            self.role[0].on = True
        elif(event.keysym == "Right"):
            self.role[0].direction = "right"
            self.role[0].on = True
        elif(event.keysym == "w"):
            self.role[1].direction = "up"
            self.role[1].on = True
        elif(event.keysym == "s"):
            self.role[1].direction = "down"
            self.role[1].on = True
        elif(event.keysym == "a"):
            self.role[1].direction = "left"
            self.role[1].on = True
        elif(event.keysym == "d"):
            self.role[1].direction = "right"
            self.role[1].on = True
        pass

    def __keyrelease(self, event):  #按键释放
        if(event.keysym == "Up"):
            self.role[0].on = False
        elif(event.keysym == "Down"):
            self.role[0].on = False
        elif(event.keysym == "Left"):
            self.role[0].on = False
        elif(event.keysym == "Right"):
            self.role[0].on = False
        elif(event.keysym == "w"):
            self.role[1].on = False
        elif(event.keysym == "s"):
            self.role[1].on = False
        elif(event.keysym == "a"):
            self.role[1].on = False
        elif(event.keysym == "d"):
            self.role[1].on = False
        pass

    def __leftclick(self, event):
        self.__continue()
        pass

    def __rightclick(self, event):
        self.on = False
        pass

    def __continue(self):  #根据游戏状态进行跳转
        if(self.state == self.game_start):
            self.state = self.game_run
        elif(self.state == self.game_run):
            self.state = self.game_pause
        elif(self.state == self.game_pause):
            self.state = self.game_run
        pass

    def start(self):  #开始游戏主循环
        self.on = True
        while self.on:
            start = time.clock()
            self.__mainloop()
            span = time.clock() - start  #计算本次循环的周期
            if(span < 1 / self.fps):
                time.sleep(1 / self.fps - span)  #尽量保证每次渲染间隔为常数，1/fps
            pass

popo = Game()
popo.start()
