'''--------------------------------------------------------------------------------
Name: Segment.py
--------------------------------------------------------------------------------
 Company: Concordia University
 Developed By : MohammadHssein AskariHemmat
 Modified Date:    11/24/2014 
 Design Name: Track segment class
 Compiler Versions: Python 2.7.5
 External Tool: NONE
 All rights reserved to HVG (http://hvg.ece.concordia.ca/)
Segments:
    DUBL_CAST_E
    CAST_E_BAYF_S
    OAKY_BAYF_S
    OAKY_SE
    OAKY_DALY
----------------------------------------------------------------------------------'''
import math
import utility
class Segment:
    def __init__(self, segName, segCivilSpeed, segGrade, segExposure,segCoordinates,color):
        self.segName = segName
        if self.segName == "DUBL_CAST_E":            
            self.segCivilSpeed = 36
            self.segGrade = 0.8
            self.segExposure = "Open"
            self.segBeginDist = 0
            self.segEndDist = 16000.1978529
        elif self.segName == "CAST_E_BAYF_S":
            self.segCivilSpeed = 80
            self.segGrade = 0.3
            self.segExposure = "Close"
            self.segBeginDist = 16000.1978529
            self.segEndDist = 19704.8957742
        elif self.segName == "OAKY_BAYF_S":
            self.segCivilSpeed = 70
            self.segGrade = 3.49
            self.segExposure = "Close"
            self.segBeginDist = 19704.8957742
            self.segEndDist = 38158.5092467
        elif self.segName == "OAKY_SE":
            self.segCivilSpeed = 50
            self.segGrade = 1.00
            self.segExposure = "Close"
            self.segBeginDist = 38158.5092467
            self.segEndDist = 38749.1571804
        elif self.segName == "OAKY_DALY":
            self.segCivilSpeed = 36
            self.segGrade = 0.8
            self.segExposure = "Open"
            self.segBeginDist = 38749.1571804
            self.segEndDist = 62690.6771109
        self.currentTrains = None
        self.nextSegments = None
        self.prevSegments = None  
        self.color = color
        self.segCoordinates = segCoordinates      
        self.segBegin = self.segCoordinates[0]
        self.segEnd = self.segCoordinates[len(self.segCoordinates)-1]
        self.segLength = utility.getTrackLength(self.segCoordinates)
        self.OutputFileData = self.segName + "_Detail.txt"  
    def __str__(self):
        return 'Segment \''+self.segName+'\'' +' CivilSpped: '\
                + str(self.segCivilSpeed)+' Grade:' + str(self.segGrade)\
                +' Exposure:'+ self.segExposure + " Color:" \
                + utility.getColor(self.color) + " Lenght: "\
                + str(round(self.segLength,2))+"meters"
    def getSegName(self):
        return self.segName

    def getSegmentCivilSpeed(self):
        return self.segCivilSpeed
    
    def getSegmentGrade(self):
        return self.segGrade
    
    def getSegCoordinates(self):
        return self.segCoordinates
    
    def getSegColor(self):
        return self.color
    
    def getEndPoint(self):
        return self.segEnd
    
    def getStartPoint(self):
        return self.segBegin
  
    def setCoordinates(self,newCoordinates):
        self.segCoordinates = []
        self.segCoordinates = newCoordinates
        
    def generateInfo(self):
        File = open(self.OutputFileData, 'wb')
        File.write("")
        File.write("Segment Name: " + self.segName + "\n")
        for coor in self.segCoordinates:   
            File.write("\t" + str(coor) + "\n")            
        File.close()    
        
    def getSegmentLength(self):
        dist = 0
        for index,item in enumerate(self.segCoordinates):
            if not(index == len(self.segCoordinates)-1):
                dist += utility.getDistance(self.segCoordinates[index][0],self.segCoordinates[index][1],self.segCoordinates[index+1][0],self.segCoordinates[index+1][1])
        return dist
    def getSegmentBeginPosition(self):
        return self.segBeginDist
    
    def getSegmentEndPosition(self):
        return self.segEndDist
    
    