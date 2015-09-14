//--------------------------------------------------------------------------------
// File name: BART.h
// Company: Concordia University
// Author : MohammadHossein Askari-Hemmat
// Design Name: BART configuration header file
// Target Devices: KL25Z128VLK4
// Date: 25/12/2014
// Platform: FRDM-KL25Z (Freescale Freedom Development Platform for Kinetis)
// Compiler Versions: Keil 5.1
// Version: 1.0
// About:
// This file contains the type decleration of BART system. All these parameters
// are taken from "Fromal Methods for Embedded Ditributed Systems" by F. Kordon 
// and M. Lemoine. 
//----------------------------------------------------------------------------


#ifndef __BART_H__
#define __BART_H__
//----------------------------------------------------------------------------
// Worst Case Scenario Distance(WCSD2) Parameters:
//----------------------------------------------------------------------------
#define pu 3.0 // Position uncertainty
#define puf 6.0 // Position uncertainty factor  
#define ad 2.0 // AATC delay   
#define tjp 1.5 // Jerk time in propulsion
#define ap 3.0 // Acceleration in propulsion
#define jp (ap/tjp) // Jerk limit in propulsion   
#define mc 1 // mode change 
#define ncar 10.0 // number of car in consist 
#define nfail 2 // number of failed cars
#define nfsmc 2 // number of cars in FSMC
#define qfsmc ((ncar-nfail-nfsmc)/(ncar))
#define brk (-1.5) // Brake rate
#define jb (-1.5) // Jerk limit braking   
#define tjb (brk/jb)
#define fsmc 8.5 // Fail safe mode change time
#define t6 (fsmc-tjp-mc-tjp)
#define bfs (brk*qfsmc)
#define q ((ncar-nfail)/(ncar))
#define vf 0 // final speed 
//----------------------------------------------------------------------------
// Gates:
//----------------------------------------------------------------------------
// Gates in BART have Name and Status. Each gate can be in 'Close' or 'Open'
// state. Gates also are located within the train path. 'gateDistance' contains
// the distance of the gate from the beginning of the path
typedef struct Gates
{
	char gateName[50];
	char gateStat[10];
	float gateDistance;
}Gate;
//----------------------------------------------------------------------------
// Segment:
//----------------------------------------------------------------------------
// Segments in BART have Name, Civil Speed, Grade, Exposure, Begin and End location.
// In our case study, we chosed a path which starts from 'DUBL_CAST_E' station to 
// 'OAKY_DALY' station. Train's speed is limited to the segment's 'civilSpeed'. 
// 'civilSpeed' is limited to 36 to 80 mph system wide. Segment 'grade' is selected 
// based on the 'segExposure' which can be either 'Open' or 'Tunnel'. Each segment
// has only one defined grade and are limited to 4% system wide. 'beginLoc' and
// 'endLoc' indicate Begin and End location of the segment according to the beginning
// of the path.
typedef struct Segments
{
	char segName[50];
	char segExposure[10];
	float civilSpeed;
	float grade;
	float beginLoc;
	float endLoc;
}Segment;
//----------------------------------------------------------------------------
// Trains:
//----------------------------------------------------------------------------
// Each control station in BART system can handle upto 10 trains at once. In
// our case study, we limited thr number of trains to two. For simplification,
// we represent a train as a single position in the map. The physical behavior 
// of a train is defined in computer end. 
typedef struct Trains
{
	char trainState[50];
	int trainID;
	float currentPosition;
	float velocity;
	float commandedVelocity;
	float acceleration;
	float commandedAcceleration;
	float nextStop;
	Segment currentSegment;
	Gate nextClosedGate;	
}Train;
//----------------------------------------------------------------------------
// Station Computer:
//----------------------------------------------------------------------------
// Each control station in BART system can handle upto 10 trains at once. In
// our case study, we limited thr number of trains to two. For simplification,
// we represent a train as a single position in the map. The physical behavior 
// of a train is defined in computer end. 
typedef struct StationComputerType
{
	char stationName[50];
	float path[5229][2];
	float velocity;
	float commandedVelocity;
	float acceleration;
	float commandedAcceleration;
	float nextStop;
	Segment currentSegment;
	Gate nextClosedGate;	
}StationComputer;
//----------------------------------------------------------------------------
// Methods:
//----------------------------------------------------------------------------
Segment getCurrentSegment(Train *train);
Train getNextTrain(Train *listOfTrains);
Gate getNextClosedGate(Train *train, Gate *listOfGates);
float getNextStop(Train *train, Gate *listOfGates);
float getWCSD2(Train *train);

#endif //BART
