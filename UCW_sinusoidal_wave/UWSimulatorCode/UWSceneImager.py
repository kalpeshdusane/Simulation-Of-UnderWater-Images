import numpy as np
import cv2 as opencv
import math
import Clock

from SceneGenerator import SceneGenerator
from UWDistSimulator import UWDistSimulator

class UWSceneImager:
    R = None
    C = None
    uwSceneGenerator = None
    uwDistSimulator = None

    def __init__(self,SceneGen, WavyPool):
        Clock.update(0)
        self.uwSceneGenerator = SceneGen
        self.uwDistSimulator =  UWDistSimulator(WavyPool,math.inf)
        self.setGrids()

    def setGrids(self):
        imSize = self.uwSceneGenerator.getFrameSize()
        X = np.array(range(imSize[1]))
        Y = np.array(range(imSize[0]))
        self.C, self.R = np.meshgrid(X, Y)

    def getUWImageAt(self,time):

        Clock.update(time)
        scene = self.uwSceneGenerator.getScene()
        imSize = scene.shape
        distX,distY = self.uwDistSimulator.getDistortions()

        mappingR = np.clip(-(-self.R + distY), 0, imSize[0] - 1)
        mappingC = np.clip(self.C + distX, 0, imSize[1] - 1)

        uwScene = self.getBiLinearInterPImage(scene,mappingR,mappingC)

        return uwScene


    def writeSimulatedVideo(self, fileName, duration, fps):

        duration = int(duration * fps)


        frameSize = self.uwSceneGenerator.getFrameSize()
        fourcc = opencv.VideoWriter_fourcc(*'MJPG')

        videoWriter = opencv.VideoWriter(fileName, fourcc, fps,(frameSize[1], frameSize[0]))

        for frameIdx in range(duration):
            distScene = 255*self.getUWImageAt(frameIdx/fps)
            videoWriter.write(distScene.astype('uint8'))

        videoWriter.release()


    def getBiLinearInterPImage(self,frame,mappingR, mappingC):

        T = np.floor(mappingR).astype(int)
        L = np.floor(mappingC).astype(int)
        R = np.floor(mappingC+1).astype(int)
        B = np.floor(mappingR+1).astype(int)

        wtTL = (B-mappingR) * (R-mappingC)
        wtTR = (B-mappingR) * (mappingC-L)
        wtBR = (mappingR-T) * (mappingC-L)
        wtBL = (mappingR-T) * (R-mappingC)

        R = np.clip(R, 0, frame.shape[1]-1)
        B = np.clip(B, 0, frame.shape[0]-1)

        imgTL = frame[T, L]
        imgTR = frame[T, R]
        imgBR = frame[B, R]
        imgBL = frame[B, L]

        interpImg = imgTL * wtTL[:,:,None] + imgTR * wtTR[:,:,None] + imgBR * wtBR[:,:,None] + imgBL * wtBL[:,:,None]
        return interpImg/255


