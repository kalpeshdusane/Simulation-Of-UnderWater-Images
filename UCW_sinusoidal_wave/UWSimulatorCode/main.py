import numpy as np

import cv2 as opencv
import  sys
sys.path.append("SparkLibrary")
import SparkTimer
import  os
from WaveGenerator import WaveGenerator
from SceneGenerator import SceneGenerator
from UWSceneImager import UWSceneImager

#default parameters
datasetFolder = '../UWSimImages'
outputFolder = '../UWSimVideos'


resolution = 1
recordingTime = 30
fps = 30
waterDepth = 25
nrWaves = 1
maxMovObjs = 9


def writeUWSimulationVideo(fileName, nrMovingObjs):
    SparkTimer.startClock()
    print('Processing file ' + fileName.split('/')[-1])
    outfile = os.path.join(outputFolder, os.path.basename(fileName).split('.')[0] + '_'+ str(nrMovingObjs) + '.avi')

    bgImg = opencv.imread(fileName)


    SceneGen = SceneGenerator(bgImg,nrMovingObjs)
    WavyPool = WaveGenerator(bgImg.shape[1]*resolution,bgImg.shape[0]*resolution,bgImg.shape,depth=waterDepth,nrWaves=nrWaves)
    UWSceneImager(SceneGen, WavyPool).writeSimulatedVideo(outfile,duration=recordingTime,fps=fps)
    SparkTimer.printElapsedTime('Completed')

def writeUWSimulationVideos(fileName, maxMovObjs):

    for i in range(maxMovObjs+1):
        writeUWSimulationVideo(fileName,i)


if __name__ == "__main__":
    #location = datasetFolder
    location = os.path.join(datasetFolder,'fish.jpg')


    if (os.path.isfile(location)):
        writeUWSimulationVideo(location, 0)
    else:
        if(os.path.isdir(location)):
            for file in os.listdir(location):
                if file.endswith(tuple([".jpg", ".png"])):
                    fileName = os.path.join(location,file)
                    outfile = os.path.join(outputFolder,file.split('.')[0]+'.avi')
                    writeUWSimulationVideos(fileName, maxMovObjs)
                    #writeUWSimulationVideo(fileName, 9)
