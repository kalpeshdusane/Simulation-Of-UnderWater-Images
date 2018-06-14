import numpy as np
import math
import random
import Clock


class WaveGenerator:
    nrWaves = 0


    depth = 10


    resolution = 0
    X = None
    Y = None

    waveParameters = None

    def __init__(self,lengthX, lengthY, gridSize, depth =25, nrWaves = 1):

        self.depth = depth
        self.nrWaves = nrWaves


        self.setCoordinates(lengthX, lengthY, gridSize)
        self.setWaveParameters(sample = 'custom')


    def setCoordinates(self, lengthX, lengthY, gridSize):
        X =  np.linspace(0,lengthX, gridSize[1])
        Y = -np.linspace(0,lengthY, gridSize[0])
        self.X,self.Y = np.meshgrid(X,Y)

    def setWaveParameters(self,sample = 'custom'):

        if(sample == 'custom'):
            waveParameters = [{'amplitude':5,'waveLen':200,'timePeriod':3,'theta': math.pi/4,'phi':0}]
        else:
            waveParameters = []
            if(sample=='random'):
                for i in range(self.nrWaves):
                    waveParameters.append(self.getRandomWave())
            else:
                if(sample=='noisyUCW'):
                    pass



        self.waveParameters = waveParameters

    def getRandomWave(self):
        A = abs(random.normalvariate(5,2))
        lam = abs(random.normalvariate(250,25))
        T = random.uniform(1, 5)
        dire = random.uniform(math.pi / 4, math.pi * 3 / 4)
        phi = random.uniform(0, math.pi)
        waveParameters = {'amplitude': A, 'waveLen': lam, 'timePeriod': T, 'theta': dire, 'phi': phi}
        return waveParameters


    def getSurfaceAndNormals(self):
        time = Clock.read()
        surface = self.getSurface(time)
        normals = self.getSurfaceNormals(time)

        return surface, normals



    def getSurface(self,t):
        Z = 0
        for w in range(self.nrWaves):
            Z = Z + self.getWaveSurface(w,t)

        return Z


    def getWaveSurface(self, idx, t):
        X,Y = self.X,self.Y
        A, kx, ky, w, phi = self.getWaveParameters(idx)
        
        Z = self.depth + A * np.sin(kx * X + ky *Y - w*t + phi)
        
        return Z

    def getSurfaceNormals(self,t):
        N = 0 
        for n in range(self.nrWaves):
            N = self.getWaveSurfaceNormals(n,t)

        norm = np.linalg.norm(N,axis=2)
        N = np.divide(N,norm[:,:,None])

        return N


    def getWaveSurfaceNormals(self, idx, t):
        X, Y = self.X, self.Y
        A, kx, ky, w, phi = self.getWaveParameters(idx)

        N = -np.ones((X.shape[0], X.shape[1],3))

        N[:,:,0] = A * kx * np.cos(kx * X + ky*Y - w*t + phi)
        N[:,:,1] = A * ky * np.cos(kx * X + ky*Y - w*t + phi)

        return N

    def getWaveParameters(self,idx):

        waveParameters = self.waveParameters[idx]

        A = waveParameters['amplitude']
        lam = waveParameters['waveLen']
        theta = waveParameters['theta']
        kx,ky = (2 * math.pi/lam)* math.cos(theta), (2 * math.pi/lam)*math.sin(theta)
        phi = waveParameters['phi']
        w = 2*math.pi / waveParameters['timePeriod']

        return A,kx,ky,w,phi
