'''--------------------------------------------------------------------------------
Name: utility.py
--------------------------------------------------------------------------------
 Company: Concordia University
 Developed By : MohammadHssein AskariHemmat
 Modified Date:    11/12/2014 
 Design Name: Utility functions
 Compiler Versions: Python 2.7.5
 External Tool: NONE
 All rights reserved to HVG (http://hvg.ece.concordia.ca/)
----------------------------------------------------------------------------------'''
import xml.etree.ElementTree as ET
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
from math import *
from Cython.Shadow import NULL
R = 6378137.0  #Earth's Radius ( in meters)    
colorList = ["#FF0000","#00FF00","#0000FF","#FFFF00","#00FFFF"]
colorListCopy = ["#FF0000","#00FF00","#0000FF","#FFFF00","#00FFFF"]
counter = 0
def getDistance(lat1,lon1,lat2,lon2):    
    lat1Rad = radians(lat1)
    lon1Rad = radians(lon1)
    lat2Rad = radians(lat2)
    lon2Rad = radians(lon2)    
    dlon = lon2Rad - lon1Rad
    dlat = lat2Rad - lat1Rad

    a = (sin(dlat/2))**2 + cos(lat1Rad) * cos(lat2Rad) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return (R * c)

def accumulativeDistance(path,latInit,lonInit):
    pathCopy = path
    if not((latInit,lonInit) in pathCopy):
        return -1
    else:
     dTemp = 0
     for index,item in enumerate(pathCopy):
        lat1 = pathCopy[index][0] 
        lon1 = pathCopy[index][1] 
        if not(index == (len(pathCopy)-1)):
            lat2 = pathCopy[index+1][0] 
            lon2 = pathCopy[index+1][1] 
            if not((lat1 == lat2) and (lon1 == lon2)):
                dTemp += getDistance(lat1,lon1,lat2,lon2)
    return dTemp
        
def getTrackLength(trackCoor):
    totalDistance = 0
    tempDistance = 0
    for index,item in enumerate(trackCoor):
        if not(index == len(trackCoor)-1):
            tempDistance = getDistance(trackCoor[index][0],trackCoor[index][1],trackCoor[index+1][0],trackCoor[index+1][1])
            totalDistance+=tempDistance
    return totalDistance
    
def getGates():
    gateList = []
    DOMTree = xml.dom.minidom.parse('/Users/Hossein/Downloads/bart.kml')
    collection = DOMTree.documentElement
    folders = collection.getElementsByTagName("Folder")
    for folder in folders:
       folderName = folder.getElementsByTagName('name')[0].childNodes[0].data
       if folderName == "BART Stations":
           placeMarks = folder.getElementsByTagName("Placemark")
           for placeMark in placeMarks:
               station = placeMark.getElementsByTagName('name')[0]
               points = placeMark.getElementsByTagName("Point")
               for point in points:                   
                   coordinates = point.getElementsByTagName('coordinates')[0].childNodes[0].data
               stationName = station.childNodes[0].data
               stationName = stationName.replace(' ','')
               stationName = stationName.replace('(','_')
               stationName = stationName.replace(')','')
               stationName = stationName.replace('.','_')
               stationName = stationName.replace('/','_')
               stationName = stationName.replace('\'','')
               stationName = stationName.replace('__','_')
               placement = coordinates.find(",")
               lon = coordinates[0:placement]
               lon = lon[0:9]
               coordinates = coordinates[placement+1:]
               placement = coordinates.find(",")
               lat = coordinates[0:placement]
               lat = lat[0:7]
               aGate = gate(stationName,float(lat),float(lon),False)
               gateList.append(aGate)

    return gateList

def trimString(string):
    string = string.replace(' ', '')
    string = string.replace('-', '_')
    string = string.replace('(', '_')
    string = string.replace(')', '')
    string = string.replace('.', '_')
    string = string.replace('/', '_')
    string = string.replace('\'', '')
    string = string.replace('__', '_')
    return string
def getColorCode(color):
    if color == 'red':
        return "#FF0000"
    elif color == 'green':
        return "#00FF00"
    elif color == 'blue':
        return "#0000FF"
    elif color == 'yellow':
        return "#FFFF00"
    elif color == 'cyan':
        return "#00FFFF"
    
def getColor(color):
    if color == "#FF0000":
        return "red"
    elif color == "#00FF00":
        return "green"
    elif color == "#0000FF":
        return "blue"
    elif color == "#FFFF00":
        return "yellow"
    elif color == "#00FFFF":
        return "cyan"
    
def getAcolor():
    global colorList,colorListCopy
    if not colorList:  
        colorList = colorListCopy
    return colorList.pop()
   
def getBearing(lat1,lon1,lat2,lon2):
    startLat = radians(lat1)
    startLong = radians(lon1)
    endLat = radians(lat2)
    endLong = radians(lon2)    
    dLong = endLong - startLong
    dPhi = log(tan(endLat/2.0+pi/4.0)/tan(startLat/2.0+pi/4.0))
    if abs(dLong) > pi:
         if dLong > 0.0:
             dLong = -(2.0 * pi - dLong)
         else:
             dLong = (2.0 * pi + dLong)
    
    bearing = (degrees(atan2(dLong, dPhi)) + 360.0) % 360.0;
    
    return (bearing)

def getPointAtDistance(lat1,lon1,d,brng):
    lat1 = radians(lat1)
    lon1 = radians(lon1) 
    brng = radians(brng)
    lat2 = asin(sin(lat1)*cos(d/R)+cos(lat1)*sin(d/R)*cos(brng))
    lon2 = lon1 + atan2(sin(brng)*sin(d/R)*cos(lat1),cos(d/R)-sin(lat1)*sin(lat2))
    lat2 = degrees(lat2)
    lon2 = degrees(lon2)
    return (lat2,lon2)

def getPointAtDistanceInPath(path,d):
    pathCopy = path
    distancePassed = 0
    inRange = False
    finalCoordinates = (-1,-1)
    dTemp = 0
    for index,item in enumerate(pathCopy):
        lat1 = pathCopy[index][0] 
        lon1 = pathCopy[index][1] 
        if not(index == (len(pathCopy)-1)):
            lat2 = pathCopy[index+1][0] 
            lon2 = pathCopy[index+1][1] 
            if not((lat1 == lat2) and (lon1 == lon2)):
                dTemp += getDistance(lat1,lon1,lat2,lon2)
            if dTemp >= d:
                inRange = True
                break
            else:
                distancePassed = dTemp
    if inRange:
        brng = getBearing(lat1,lon1,lat2,lon2)
        finalCoordinates = getPointAtDistance(lat1,lon1,(d-distancePassed),brng)
    return finalCoordinates

def getTraveledDistanceInPath(path,pos):
# returns the distance of POS from the beginning of PATH
    d = 0
    for point in path:
        if (point[0] == pos[0]) and (point[1] == pos[1]):
            d += getDistance(point[0],point[1],pos[0],pos[1]) 
            return d
        else:
            d += getDistance(point[0],point[1],pos[0],pos[1]) 
            
def inTrack(track,gate,precision):
    global counter
    distance = 0
    for pointIntrack in track:
        distance = getDistance (pointIntrack[0],pointIntrack[1],gate[0],gate[1])
        counter+=1
        if distance < precision:
            return True
    return False

def getTraveledDistance(path,loc):
    dTemp = 0
    for index,item in enumerate(path):
        inPath = ((path[index][0] == loc[0]) and (path[index][1] == loc[1]))
        if not(index == (len(path)-1)):
            if ((180 - getBearing(path[index][0],path[index][1],loc[0],loc[1])) > 0) and not (inPath):
                dTemp += getDistance(path[index-1][0],path[index-1][1],loc[0],loc[1])
                return dTemp
            elif inPath:
                dTemp+=0
                return dTemp
            else:
               # if (getDistance(path[index][0],path[index][1],loc[0],loc[1]) > getDistance(path[index][0],path[index][1],path[index+1][0],path[index+1][1])):
                    dTemp += getDistance(path[index][0],path[index][1],path[index+1][0],path[index+1][1])
        else:
            return dTemp
    return 0
        