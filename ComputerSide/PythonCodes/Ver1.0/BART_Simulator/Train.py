'''--------------------------------------------------------------------------------
Name: train.py
--------------------------------------------------------------------------------
 Company: Concordia University
 Developed By : MohammadHssein AskariHemmat
 Modified Date:    11/28/2014 
 Design Name: Train class
 Compiler Versions: Python 2.7.5
 External Tool: NONE
 All rights reserved to HVG (http://hvg.ece.concordia.ca/)
----------------------------------------------------------------------------------'''
import math
import utility
from Cython.Shadow import NULL
from rsa.util import private_to_public
#==============================================================================================================
# Class Train:
#==============================================================================================================
class train:
#==============================================================================================================
# Global Variables:
#==============================================================================================================
    deltaTime = 0.5
    gradeAcc = 0
#==============================================================================================================
# Constructor:
#==============================================================================================================           
    def __init__(self,nosePosition,velocity,acceleration,Id,segmentList,path,gateList):
        self.nosePosition = nosePosition
        self.path = path
        self.traveledDistance = utility.getTraveledDistance(path,nosePosition)
        self.velocity = velocity
        self.acceleration = acceleration
        self.Id = Id
        self.deltaX = 0
        self.locationHistory = []
        self.commandedVelocity = 2
        self.commandedAcceleration = 2
        self.Image = "/Users/Hossein/Dropbox/steamtrain.png"  
        self.latFilePath = ("LAT_COOR_"+str(self.Id)+".dat")
        self.lonFilePath = ("LON_COOR_"+str(self.Id)+".dat")
        self.segmentList = segmentList
        self.currentSegment = segmentList[0]
        self.gateList = gateList
        self.state = 'Stop'
        self.Name = "Train_"+str(self.Id)
    def __str__(self):
        return self.getName()+\
               " a: " +str(self.acceleration)+" v: "+ \
               str(self.velocity) + " acm: " +str(self.commandedAcceleration)+\
               " vcm: " +str(self.commandedVelocity)+" Seg: " + self.getCurrentSegment().getSegName()+\
               "  TD:" + str(self.traveledDistance) + " deltaX: " + str(self.deltaX)+\
               " Grade:" + str(self.getCurrentSegment().getSegmentGrade()) + " State:" + self.getState() 

#==============================================================================================================
# Methods:
#==============================================================================================================           
    def getName(self):
        return self.Name
    def getPosition(self):
        return self.nosePosition
    def getVelocity(self):
        return self.velocity
    def getAcceleration(self):
        return self.acceleration
    def getTrainId(self):
        return self.Id
    def getImage(self):
        return self.Image
    def getCommandedAcc(self):
        return self.commandedAcceleration
    def getCommandedVel(self):
        return self.commandedVelocity
    def updateCommandedVel(self,commandedVel):
        self.commandedVelocity = commandedVel
    def updateCommandedAcc(self,commandedAcc):
        self.commandedAcceleration = commandedAcc
    def getTraveledDistance(self):
        return self.traveledDistance    
    def getLocationHistory(self):
        return self.locationHistory    
    
    def update(self):
        global deltaTime
        # Updating train's position
        gradeAcc = -21.9*(self.currentSegment.getSegmentGrade()/100.0)
        x = (self.velocity * self.deltaTime) + ((0.5) * self.acceleration * self.deltaTime * self.deltaTime) + ((0.5) * gradeAcc * self.deltaTime * self.deltaTime)
        self.deltaX = x
        if (self.velocity == 0) and (self.commandedVelocity == 0):
            self.nosePosition = self.nosePosition
        else:
            self.traveledDistance += x
            (self.locationHistory).append(self.traveledDistance)
            self.nosePosition = utility.getPointAtDistanceInPath(self.path,self.traveledDistance)

        # Updating train's Velocity
        speed  = self.velocity + ((0.5)*self.acceleration*self.deltaTime) + ((0.5)*gradeAcc*self.deltaTime)
        if ((self.velocity == 0) and (self.commandedVelocity == 0)) or (speed<0):
            self.velocity = 0
        else:
            self.velocity = speed
            
        # Updating train's Acceleration
        if (self.velocity == 0) and (self.commandedVelocity == 0):
            self.acceleration = 0
        elif ((self.velocity > (self.commandedVelocity -2)) and (self.commandedAcceleration>0)) or ((self.velocity < (self.commandedVelocity - 2)) and (self.commandedAcceleration < 0)):
            self.acceleration = 21.9*(self.currentSegment.getSegmentGrade()/100.0)
        else:
            self.acceleration = self.commandedAcceleration
            
        latFile = open(self.latFilePath, 'wb')
        latFile.write("")
        latFile.write(str(self.nosePosition[0]))    
        latFile.close()

        lonFile = open(self.lonFilePath, 'wb')
        lonFile.write("")
        lonFile.write(str(self.nosePosition[1]))     
        lonFile.close()    
        print self
        
    def getCurrentSegment(self):
        for segment in self.segmentList:
            dBegin = segment.getSegmentBeginPosition()
            dEnd = segment.getSegmentEndPosition()
            dNosePosition = utility.getTraveledDistance(self.path,self.nosePosition)
            if (dNosePosition > dBegin) and (dNosePosition < dEnd):
                return segment
        print "ERROR!"
                
    def getState(self):
        if (self.acceleration > 0) and not(self.velocity == 0):
            self.state = "Propulsion"
            return self.state
        elif (self.acceleration == 0) and (self.velocity > 0):
            self.state = "Normal"
            return self.state
        elif (self.acceleration == 0) and (self.velocity == 0):
            self.state = "Stop"
            return self.state
        elif (self.acceleration <= -0.45) and (self.acceleration >= -2):
            self.state = "Brake"
            return self.state
        else:
            self.state = "INVALID"
            return self.state
                
    def getCurrentPosition(self):
        return utility.getTraveledDistance(self.path,self.getPosition())
        
    def nextSegmentsInRange(self,range):
        upcommingSegments = []
        potentialSegments = []
        counter = 0
        for segment in self.segmentList:
            if segment.getSegName() == self.getCurrentSegment().getSegName():
                currentSegNumber = counter                
                break
            counter+=1
        segments = self.segmentList[counter:]
        potentialSegments.extend(segments)
        
        for segment in potentialSegments:        
             distance = (segment.getSegmentBeginPosition() - utility.getTraveledDistance(self.path,self.getPosition()))
             if (distance < 0) or  (distance <= range):
                 upcommingSegments.append(segment)
        return upcommingSegments
                                                    