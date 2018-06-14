import numpy as np
import math
from WaveGenerator import WaveGenerator

No_call = 0
avg_norm_x = 0
avg_norm_y = 0

class UWDistSimulator:


    cameraHt = 0
    waveGenerator = None
    refIdx = 4/3

    def __init__(self, waveGen, cameraHt):

        self.cameraHt = cameraHt
        self.waveGenerator = waveGen

    def getDistortions(self):
        surface, N = self.waveGenerator.getSurfaceAndNormals()
        I = self.getIncidentRays(surface)
        n = self.refIdx
        #vector eqn refration : n*r - i = -N(n*cos(r) - cos(i))
        cosI = np.sum(np.multiply(-N,I),axis=2)
        cosR = np.sqrt(1 - 1/(n**2) + np.power(cosI/n,2))

        R = n * (I + np.multiply(-N,(n * cosR - cosI)[:,:,None]))
        R = np.divide(R,(R[:,:,2])[:,:,None])

        distortionX = np.multiply(R[:,:,0] , surface)
        distortionY = np.multiply(R[:,:,1] , surface)

        global No_call
        global avg_norm_x,avg_norm_y
        x = 100
        y = 120
        No_call = No_call + 1
        avg_norm_x = avg_norm_x + distortionX[x,y]
        avg_norm_y = avg_norm_y + distortionY[x,y]
        print("time : ",No_call,"\t distortion_X : ",distortionX[x,y]," Avg_x : ", avg_norm_x/No_call)
        print("\t\t distortion_Y : ",distortionY[x,y]," Avg_y : ",avg_norm_y/No_call)

        return distortionX, distortionY



    def getIncidentRays(self, surface = None):

        if(math.isinf(self.cameraHt)):
            gridSize = surface.shape
            iRays = np.zeros((gridSize[0], gridSize[1], 3))
            iRays[:,:,2] = -1
        else:
            iRays = None #implement perspective projection

        return iRays