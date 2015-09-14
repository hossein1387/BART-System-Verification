'''--------------------------------------------------------------------------------
Name: BART.py
--------------------------------------------------------------------------------
 Company: Concordia University
 Developed By : MohammadHssein AskariHemmat
 Modified Date:    11/12/2014 
 Design Name: BART Simulator
 Compiler Versions: Python 2.7.5
 External Tool: NONE
 All rights reserved to HVG (http://hvg.ece.concordia.ca/)
----------------------------------------------------------------------------------'''
import xml.etree.ElementTree as ET
import simpleguitk as simplegui
import utility
import Segment
import Train
import Gate
import StationComputer
from math import *
import pygmaps 
import subprocess, os
import time
import mechanize
import serial
from __builtin__ import int
from elementtree.ElementTree import ElementTree 
from xml.etree.ElementTree import parse
from findertools import sleep
from xml.dom.minidom import parse
import xml.dom.minidom
from _imaging import path
import binascii
import sys
import select

#==============================================================================================================
# globals for user interface:
#==============================================================================================================           
WIDTH = 1000
HEIGHT = 800  
R = 6378137.0 
X = 0
Y = 1
gateList = []
trackList = []
LAT_FILE_PATH = "LAT_COOR.dat"
LON_FILE_PATH = "LON_COOR.dat"
GATE_STAT_PATH = "Gates.txt"
PATH_DATA_FILE_DIR = "path.h"
SEGMENT_DATA_FILE_DIR = "path.h"
GATE_DATA_FILE_DIR = "path.h"
trackLonCoordinateListFinal = []
trackLatCoordinateListFinal = []
segmentList = []
trainList = []
trackStations = []
trackCoordinates = []
#==============================================================================================================
# Internal Functions:
#==============================================================================================================           
def getSegments():
    global trackList,trackCoordinates,mymap
    fileName = "BARTRoutes.txt"
    f = open(fileName, 'wb')
    counter = 0
    coordinates = ""
    coordinationsStr = ""
    DOMTree = xml.dom.minidom.parse('/Users/Hossein/Downloads/bart.kml')
    collection = DOMTree.documentElement
    folders = collection.getElementsByTagName("Folder")
    for folder in folders:
       folderName = folder.getElementsByTagName('name')[0].childNodes[0].data
       if folderName == "BART Tracks":
           placeMarks = folder.getElementsByTagName("Placemark")
           for placeMark in placeMarks:
               routName = placeMark.getElementsByTagName('name')[0].childNodes[0].data
               if routName == "DUBL-DALY (ROUTE 11/12)":                   
                   multiGeometries = placeMark.getElementsByTagName("MultiGeometry")
                   for geometry in multiGeometries:
                       Linestrings = geometry.getElementsByTagName("LineString")
                       trackLatCoordinateList = []
                       trackLonCoordinateList = []
                       trackName = placeMark.getElementsByTagName('name')[0].childNodes[0].data
                       trackName = utility.trimString(trackName)
                       print trackName
                       for lineString in Linestrings:
                           routName = utility.trimString(lineString.getAttribute('id'))
                           #print '\t' + utility.trimString(routName)
                           coordinates = lineString.getElementsByTagName("coordinates")[0].childNodes[0].data
                           coordinates = coordinates.replace(',0',',')
                           coordinates = coordinates.replace('\n','')
                           coordinationsStr += " "+coordinates
                           coordinates = []     
                           num1 = ""
                           num2 = ""
                           newNumber1 = True
                           newNumber2 = False
                           for chr in coordinationsStr:
                               if newNumber1:
                                   if not(chr == ",") and not(chr == " "):
                                       num1+=chr
                                       continue
                                   elif (chr == ","):
                                       newNumber2 = True
                                       newNumber1 = False                                       
                                       data = round(float(num1),6)
                                       trackLonCoordinateList.append(data)
                                       num1 = ""
                                       continue
                               if newNumber2:
                                   if not(chr == " "):
                                       num2+=chr
                                       continue
                                   else:
                                       data = round(float(num2),6)
                                       trackLatCoordinateList.append(data)
                                       num2 = ""
                                       newNumber2 = False
                                       newNumber1 = True
                                       continue                            
                           coordinationsStr = []
                           trackList = []
                           trackBeginCoor = []
                           trackEndCoor = []
                           for index,item in enumerate(trackLatCoordinateList):
                               trackList.append((trackLatCoordinateList[index],trackLonCoordinateList[index]))                          
                           if (routName == 'OAKY_BAYF_S') or (routName == 'OAKY_DALY'):  
                               trackList = trackList[::-1]
                           trackLatCoordinateList = []
                           trackLonCoordinateList = []
                           if (routName == 'OAKY_SE') or (routName == 'OAKY_DALY'):  
                               segment = Segment.Segment(routName, 60, 2, "Tunnel",trackList,utility.getAcolor())  
                           else:
                               segment = Segment.Segment(routName, 80, 2, "Open",trackList,utility.getAcolor())                                 
                           segmentList.append(segment)
    totalDistance = 0
    for segments in segmentList:
        path = []
        path = segments.getSegCoordinates()
        mymap.addpath(segments.getSegName(),path,segments.getSegColor()) 
        for coor in path:
            trackCoordinates.append(coor)
        totalDistance +=segments.getSegmentLength()
#==============================================================================================================

def savePathFile(path):
    PATH_DATA_FILE = open(PATH_DATA_FILE_DIR, 'wb')
    PATH_DATA_FILE.write("#ifndef __PATH_H__\n#define __PATH_H__\n")
    PATH_DATA_FILE.write("extern int path[5229][2] = {\n")
    for index,item in enumerate(path):
        if index == len(path)-1:            
            PATH_DATA_FILE.write(str("\t"+"{"+str(path[index][0]))+","+str(path[index][1])+"}"+"\n")     
        else:
            PATH_DATA_FILE.write(str("\t"+"{"+str(path[index][0]))+","+str(path[index][1])+"},"+"\n")                 
    PATH_DATA_FILE.write("}\n")
    PATH_DATA_FILE.write("#endif //__PATH_H__\n")
    PATH_DATA_FILE.close()    
#==============================================================================================================    
def getGates():
    global trackStations,trackCoordinates
    counter = 0
    coordinationsStr = ""
    coordinates  = []
    stationLoc = []
    DOMTree = xml.dom.minidom.parse('/Users/Hossein/Downloads/bart.kml')
    collection = DOMTree.documentElement
    folders = collection.getElementsByTagName("Folder")
    #print "Gates in Track: "
    for folder in folders:
       folderName = folder.getElementsByTagName('name')[0].childNodes[0].data
       if folderName == "BART Stations":
           placeMarks = folder.getElementsByTagName("Placemark")
           for placeMark in placeMarks:
               coordinationsStr = placeMark.getElementsByTagName("coordinates")[0].childNodes[0].data  
               coordinationsStr = coordinationsStr.replace(',0','')
               coordinates = coordinationsStr.split(',')
               stationName = placeMark.getElementsByTagName("name")[0].childNodes[0].data
               stationLat = float(coordinates[1])
               stationLon = float(coordinates[0])        
               stationLoc = [stationLat,stationLon]
               loc = utility.getTraveledDistance(trackCoordinates,stationLoc)
               if utility.inTrack(trackCoordinates,stationLoc,300):
                   counter+=1
                   gate = Gate.Gate(stationName, stationLat,stationLon,True,loc,counter)    
                   gateList.append(gate)                   
               
#==============================================================================================================
def updateMap():
    global trainList,stationComputer
    stationComputer.update()

#==============================================================================================================
def updateGates():
    global gateList
    for gate in gateList:
        gate.update()
#==============================================================================================================
def update():
    train1.updateCommandedVel(float(serialPort.readline()))
    train1.updateCommandedAcc(float(serialPort.readline()))
    serialPort.write(str(train1.getVelocity())+"\n")
    serialPort.write(str(train1.getAcceleration())+"\n")
    serialPort.write(str(train1.getCurrentPosition())+"\n")
    train1.update()
#==============================================================================================================
# Main Program:
#==============================================================================================================     
mymap = pygmaps.maps(37.7016, -121.9003, 16)
getSegments()
getGates()
savePathFile(trackCoordinates)
totalDistance = 0
for gate in gateList:
    if gate.getGateStatStr() == 'open':
        mymap.addpoint(gate.getGateLat(),gate.getGateLon(), gate.getName(), utility.getColorCode("green"))
    else:
        mymap.addpoint(gate.getGateLat(),gate.getGateLon(),gate.getGatename(), utility.getColorCode("red"))        
for seg in segmentList:
    dBegin = utility.getTraveledDistance(trackCoordinates,seg.getStartPoint())
    dEnd = utility.getTraveledDistance(trackCoordinates,seg.getEndPoint())

#==============================================================================================================     
# Create a StationComputer Obj:
#==============================================================================================================     
stationComputer = StationComputer.StationComputer(trainList,segmentList,trackCoordinates,gateList)
#==============================================================================================================     
# Create a Train and add it to map:
#==============================================================================================================     
initialPos1 = utility.getPointAtDistanceInPath(trackCoordinates,30)

train1 = Train.train(initialPos1,0,2,1,segmentList,trackCoordinates,gateList) 
trainList.append(train1)
mymap.addTrain(initialPos1[0], initialPos1[1], 1)
mymap.draw('./mymap.html')
#==============================================================================================================     
# Create a timer and opening Google maps
#==============================================================================================================     
timer = simplegui.create_timer(100, update)
timer.start()

#==============================================================================================================     
# Establishing a Serial port
#==============================================================================================================     
serialPort = serial.Serial(port='/dev/tty.usbmodem14121', baudrate=115200)

os.system("open "+'/Applications/Google\ Chrome.app ./mymap.html --args --allow-file-access-from-files')
