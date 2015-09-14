'''--------------------------------------------------------------------------------
Name: StationComputer.py
--------------------------------------------------------------------------------
 Company: Concordia University
 Developed By : MohammadHssein AskariHemmat
 Modified Date:    11/28/2014 
 Design Name: Train class
 Compiler Versions: Python 2.7.5
 External Tool: NONE
 All rights reserved to HVG (http://hvg.ece.concordia.ca/)
----------------------------------------------------------------------------------'''
from math import pow
import utility
import os.path
from Cython.Shadow import NULL
#==============================================================================================================
# Class Train:
#==============================================================================================================
class StationComputer:
#==============================================================================================================
# Worst Case Scenario Distance(WCSD2) Parameters:
#==============================================================================================================
    pu = 3.0 # Position uncertainty  
    puf = 6.0 # Position uncertainty 
    ad = 2.0 # AATC delay            
    tjp = 1.5 # Jerk time in propulsi
    ap = 3.0 # Acceleration in propul
    jp = (ap/tjp) # Jerk limit in pro
    mc = 1 # mode change             
    ncar = 10.0 # number of car in co
    nfail = 2 # number of failed cars
    nfsmc = 2 # number of cars in FSM
    qfsmc = ((ncar-nfail-nfsmc)/(ncar))
    brk = (-1.5) # Brake rate        
    jb = (-1.5) # Jerk limit braking 
    tjb = (brk/jb)                    
    fsmc = 8.5 # Fail safe mode chang
    t6 = (fsmc-tjp-mc-tjb)            
    bfs = (brk*qfsmc)                 
    q = ((ncar-nfail)/(ncar))         
    vf = 0 # final speed                 
#==============================================================================================================
# Global Variables:
#==============================================================================================================
    deltaTime = 0.5
    gradeAcc = 0
    A_DATA_FILE_DIR = "ACCELERATION.txt"
    POS_DATA_FILE_DIR = "POSITION.txt"
    V_DATA_FILE_DIR = "VELOCITY.txt"
    
#==============================================================================================================
# Constructor:
#==============================================================================================================           
    def __init__(self,trainList,segments,path,gateList):
        self.trainList = trainList
        self.segments = segments
        self.path = path
        self.gateList = gateList
        if (os.path.exists(self.A_DATA_FILE_DIR)):
            os.remove(self.A_DATA_FILE_DIR)
        if (os.path.exists(self.POS_DATA_FILE_DIR)):
            os.remove(self.POS_DATA_FILE_DIR)
        if (os.path.exists(self.V_DATA_FILE_DIR)):
            os.remove(self.V_DATA_FILE_DIR)
    def __str__(self):
        return "#Trains: " + str(len(self.trainList))
#==============================================================================================================
# Methods:
#==============================================================================================================           
    def getWCSD2(self,train):        
        d1 = self.puf * self.pu
        d2 = train.getVelocity()*self.ad
        a = -4
        d3 = train.getVelocity()*self.tjp + (0.5)*self.ap*self.tjp*self.tjp + (0.1666667)*self.jp*self.tjp*self.tjp*self.tjp + (0.5)*a*self.tjp*self.tjp
        v3 = train.getVelocity() + self.ap*self.tjp + (0.5)*self.jp*self.tjp*self.tjp + a*self.tjp        
        d4 = v3*self.mc + (0.5)*a*self.mc*self.mc
        v4 = v3 + a*self.mc
        d5 = v4*self.tjb + (0.1666667)*self.jb*self.qfsmc*self.tjb*self.tjb*self.tjb + (0.5)*a*self.tjb*self.tjb        
        v5 = v4 + (0.5)*self.jb*self.qfsmc*self.tjb*self.tjb + a*self.tjb
        d6 = v5*self.t6 + (0.5)*self.bfs*self.t6*self.t6 + (0.5)*a*self.t6*self.t6
        v6 = v5 + self.bfs*self.t6 + a*self.t6
        d7 = (self.vf*self.vf - v6*v6)/(2*(self.brk*self.q + a))
        return d1+d2+d3+d4+d5+d6+d7
    
    def getListOfTrains(self):
        return self.trainList
    def getListOfSegments(self):
        return self.segments
    def getPath(self):
        return self.path
    def getListOfGates(self):
        return self.gateList
    def getClosestObjDistace(self,train):
        pass
    
    def getCivilSpeed(self,train,range):
        segments = train.nextSegmentsInRange(range)
        speed = 10000
        civilSpeedSegment = []
        for segment in segments:
            if segment.getSegmentCivilSpeed() < speed:
                speed = segment.getSegmentCivilSpeed()
                civilSpeedSegment = segment
        return civilSpeedSegment
    
    def getTrainsAhead(self,train,currentPos):
        trainsAhead = []
        for trains in self.trainList:
            pos = trains.getCurrentPosition()
            if (pos - currentPos) > 0:
                trainsAhead.append(trains)
        return trainsAhead
    
    def getGatesAhead(self,train,currentPos):
        gatesAhead = []
        for gate in self.gateList:
            pos = gate.getGateLocation()
            if (pos - currentPos) > 0:
                gatesAhead.append(gate)
        return gatesAhead
    
    def getNextStop(self,train):
        currentPosition = train.getCurrentPosition()
        minDistanceToTrain = 65000
        minDistanceToGate = 65000
        nextGate = []
        nextTrain = []
        trainsAhead = self.getTrainsAhead(train,currentPosition)
        gatesAhead = self.getGatesAhead(train,currentPosition)
        
        for trains in trainsAhead:
            if trains.getTrainId() != train.getTrainId():
                if trains.getCurrentPosition() < minDistanceToTrain:
                    minDistanceToTrain = trains.getCurrentPosition()
                    nextTrain = train
        for gate in gatesAhead:
            if gate.getGateLocation() < minDistanceToGate:
                minDistanceToGate = gate.getGateLocation()
                nextGate = gate
                
        if minDistanceToGate < minDistanceToTrain:
            return minDistanceToGate,nextGate
        else:
            return minDistanceToTrain,nextTrain

        
    def LogData(self,a,v,pos):
        A_DATA_FILE = open(self.A_DATA_FILE_DIR, 'a')
        V_DATA_FILE = open(self.V_DATA_FILE_DIR, 'a')
        POS_DATA_FILE = open(self.POS_DATA_FILE_DIR, 'a')
        A_DATA_FILE.write(str(a)+"\n")
        V_DATA_FILE.write(str(v)+"\n")
        POS_DATA_FILE.write(str(pos)+"\n")
            
#==============================================================================================================
# Control Algorithm:
#==============================================================================================================           
    def update(self):
        global deltaTime
        for train in self.trainList:
#==============================================================================================================           
# calculating BART parameters:
            wcsd2 = self.getWCSD2(train)
            range = wcsd2*2 + 138
            gradeacc = -21.9 * train.getCurrentSegment().getSegmentGrade()/100.0
            acc = 0
#==============================================================================================================           
# calculating new commanded velocity:
            nextStopDistance,nextObj = self.getNextStop(train)
            minCivilSpeedSegment = self.getCivilSpeed(train,range)
            vcmCivilSpeed = minCivilSpeedSegment.getSegmentCivilSpeed()                
            trainPosition = train.getCurrentPosition()
            if (nextStopDistance - trainPosition) < range:
                commandedSpeed = 0
            else:
                commandedSpeed = vcmCivilSpeed
#==============================================================================================================           
# calculating "acmCivilSpeed"           
            d1 = (minCivilSpeedSegment.getSegmentBeginPosition()) - trainPosition
            if d1 < 0:
                acc = train.getAcceleration() + 0.5
            else:
                acc = ((pow(vcmCivilSpeed-2,2) - pow(train.getVelocity(),2))/2*d1) - gradeacc
            if acc<0 and acc>-0.45 :
                acmCivilSpeed = -0.45
            else:
                acmCivilSpeed = acc
#==============================================================================================================           
# calculating "acmNextStop"           
            d2 = nextStopDistance - trainPosition - wcsd2
            acc = ((-1*pow(train.getVelocity(),2))/2*d2) - gradeacc
            if (nextStopDistance-trainPosition) > range:
                acmNextStop = train.getAcceleration() + 0.5
            else:
                if (acc<0 and acc>-0.45) and (d2>((train.getVelocity()*self.deltaTime)+0.5*gradeacc*pow(self.deltaTime,2))):
                    acmNextStop = 0
                elif( (acc<0 and acc>-0.45) and (d2<=((train.getVelocity()*self.deltaTime)+0.5*gradeacc*pow(self.deltaTime,2)))):
                    acmNextStop = -0.45
                else:
                    acmNextStop = acc
#==============================================================================================================           
# calculating "acm" using "acmNextStop" and "acmCivilSpeed":
            if acmCivilSpeed<acmNextStop:
                acm = acmCivilSpeed
            else:
                acm = acmNextStop          
#==============================================================================================================           
# Making sure acm is in the acceleration window:
            if acm < (-2.0):
                acm = -2.0
            elif acm > 3:
                acm = 3
            elif acm < 0 and (acm > -0.45):
                acm = -0.45
            elif train.getVelocity() <= 0.5 and commandedSpeed == 0:
                acm = -2.0
            else:
                acm = acm
#==============================================================================================================           
# Updating new commanded velocity and acceleration:                
            commandedAcc = acm             
            train.updateCommandedVel(commandedSpeed)
            train.updateCommandedAcc(commandedAcc)
            train.update()
        
        
        
        
        
        
        
        
        
        
        
            