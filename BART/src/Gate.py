'''--------------------------------------------------------------------------------
Name: gate.py
--------------------------------------------------------------------------------
 Company: Concordia University
 Developed By : MohammadHssein AskariHemmat
 Modified Date:    11/12/2014 
 Design Name: Gate class
 Compiler Versions: Python 2.7.5
 External Tool: NONE
 All rights reserved to HVG (http://hvg.ece.concordia.ca/)
----------------------------------------------------------------------------------'''
from math import *
import random
import utility
offTime = 30 #for 30 seconds the gate is closed
onTime = 100 #for 30 seconds the gate is open
class Gate:
    def __init__(self,gateName,gateLat,gateLon,open,loc,Id):
        self.localTimer = random.randint(1,onTime)
        self.gateName = gateName
        self.gateLat = gateLat
        self.gateLon = gateLon
        self.gateLocation = loc
        self.Id = Id
        self.open = open
    def __str__(self):
        if self.open:
            return 'Gate \''+self.gateName+'\'' + ' is located at ' +str(self.gateLocation)+' is Open'
        else:
            return 'Gate \''+self.gateName+'\'' + ' is located at ' +str(self.gateLocation)+' is Close'           

    def getGateStat(self):
        return self.open
    def getGateId(self):
        return self.Id
    def setGateStat(self,stat):
        self.open = stat
    def getName(self):
        return self.gateName
    def getGatePos(self):
        return [self.gateLat,self.gateLon]
    def getGateLocation(self):
        return self.gateLocation
    def getGateStatStr(self):
        if self.open:
            return "open"
        else:
            return "close"
    def getGateLat(self):
        return self.gateLat
    def getGateLon(self):
        return self.gateLon
    def update(self):
        self.localTimer += 1
        if self.open:
            if self.localTimer >= onTime:
                self.open = False
                self.localTimer = 0
        elif not (self.open):
            if self.localTimer >= offTime:
                self.open = True
                self.localTimer = 0
        print self
            
            
            
        
    