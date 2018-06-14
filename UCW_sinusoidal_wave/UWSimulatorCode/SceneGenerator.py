from scipy.interpolate import interp1d
import numpy as np
import random
import math
import Clock

class RandomPath:

    Rt = None
    Ct = None
    VMin, VMax = 5,50

    def __init__(self, motionBounds, clearance, duration):

        self.VMax = math.sqrt(motionBounds[0]**2 + motionBounds[1]**2)/duration
        support = 6
        rows, rTime = self.getBounded1DPath(clearance, motionBounds[0] - clearance, support, duration)
        cols, cTime = self.getBounded1DPath(clearance, motionBounds[1] - clearance, support, duration)
        self.Rt = interp1d(rTime,rows, kind='linear')
        self.Ct = interp1d(cTime,cols, kind='linear')

    def getBounded1DPath(self,lower,upper, support, duration):

        path = np.random.uniform(lower,upper,support)
        dists = np.cumsum(np.abs(path[1:] - path[0:-1]))
        time  = np.append([0],duration * dists/dists[-1])

        return path, time

    def getLocation(self,time):

        r = int(self.Rt(time))
        c = int(self.Ct(time))

        return r,c


class MovingObject:
    path = None
    length = 0
    checkLen = 0
    img = None
    centreR, centreC = 0,0


    def __init__(self, length, motionBounds, margin, duration):

        self.path = RandomPath(motionBounds, margin, duration)
        self.length = 2*(length//2)
        self.setAppearence()

    def setAppearence(self):
        img = np.zeros((self.length, self.length, 3))

        X = np.array(range(self.length))
        Y = np.array(range(self.length))
        C, R = np.meshgrid(X, Y)
        self.checkLen = self.length//2

        C = C//self.checkLen
        R = R//self.checkLen

        whites = (C%2)==(R%2)
        img[whites,:] = 255

        self.img = img

    def getAppearance(self):
        return self.img

    def getBounds(self):
        time = Clock.read()
        centreR, centreC = self.path.getLocation(time)
        rT = centreR - self.length/2
        rB = centreR + self.length/2

        cL = centreC - self.length/2
        cR = centreC + self.length/2

        return int(rT), int(cL), int(rB), int(cR)

class SceneGenerator:
    bgImg = None

    randomPath = None


    def __init__(self, image, nrMovObjs, objLen = 50, motionTime = 30):
        self.bgImg = image.copy()
        self.movingObjects = [MovingObject(objLen,image.shape,objLen+5, motionTime) for _ in range(nrMovObjs)]

    def getFrameSize(self):
        return self.bgImg.shape

    def paintObject(self, MovingObj, scene):
        rT, cL, rB, cR = MovingObj.getBounds()
        scene[rT:rB,cL:cR,:] = MovingObj.getAppearance()


    def getScene(self):

        scene = self.bgImg.copy()

        for object in self.movingObjects:
            self.paintObject(object, scene)


        return scene










        
