//--------------------------------------------------------------------------------------------
// This file was automatically generated by SysMLToRTX tool
//--------------------------------------------------------------------------------------------
// Company: Concordia University
// Author : MohammadHossein Askari-Hemmat
// Target Devices: KL25Z128VLK4
// Platform: FRDM-KL25Z (Freescale Freedom Development Platform for Kinetis)
// Compiler Versions: Keil 5.1
// RTOS: RTX 4.74 From Keil
// Version: 1.1 (Concurrency and thread creation is supported in this version)
// Original diagram can be found in: /Users/Hossein/Documents/Topcased/ComputerStation/Models/ComputerStation
// Date: 2015/01/03  08:43:07
//--------------------------------------------------------------------------------------------
#include <MKL46Z4.h>
#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include "Bart.h"
#include "mcg.h"
#include "freedom.h"
#include "common.h"
#include "uart.h"
//============================================================================================
//Methods Prototype:
void InitialNode1_method(void);
void cpuInitialization_method(void);
void ActivityFinalNode1_method(void);
void calculateRange_method(void);
void getCurrentSegmentGrade_method(void);
void calculateWCSD2_method(void);
void getNextStopDistance_method(void);
void getCivilSpeed_method(void);
void D1_method(void);
void resetCommandedSpeed_method(void);
void updateCommandedSpeed_method(void);
void calculateAcmCivilSpeed_method(void);
void calculateAcmNextStop_method(void);
void DecisionNode2_method(void);
void assignAcmNextStopToAcm_method(void);
void assignAcmCivilSpeedToAcm_method(void);
void checkAcmBounderies_method(void);
void sendNewCommands_method(void);
void waitToreceiveNewData_method(void);
void D3_method(void);
//============================================================================================
//Variable Decleration:
bool InitialNode1_var = true;
bool cpuInitialization_var = false;
bool ActivityFinalNode1_var = false;
bool calculateRange_var = false;
bool getCurrentSegmentGrade_var = false;
bool calculateWCSD2_var = false;
bool getNextStopDistance_var = false;
bool getCivilSpeed_var = false;
bool D1_var = false;
bool inRange = false;
bool resetCommandedSpeed_var = false;
bool updateCommandedSpeed_var = false;
bool calculateAcmCivilSpeed_var = false;
bool calculateAcmNextStop_var = false;
bool DecisionNode2_var = false;
float acmNextStop;
float acmCivilSpeed;
bool assignAcmNextStopToAcm_var = false;
bool assignAcmCivilSpeedToAcm_var = false;
bool checkAcmBounderies_var = false;
bool sendNewCommands_var = false;
bool waitToreceiveNewData_var = false;
bool D3_var = false;
char command[] = "CONTINUE";
char message[20];
//----------------------------------------------------------------------------
// Global variables:
//----------------------------------------------------------------------------
Gate gateList[numberOfGates];
Segment segmentList[numberOfSegments];
Train trainlists[numberOfTrains];
int counter = 0;
//============================================================================================
int main (void){
	InitialNode1_method();
	return 0;
}

//============================================================================================
//Methods Decleration:
void InitialNode1_method(){
	StationComputer stationComputer;
//	stationComputer.stationName = "BART_STATION_COMPUTER";
	generateGateList();
	generateSegmentList();
	initializeTrain();
	cpuInitialization_method();//Calling the appropriate method
 }

void cpuInitialization_method(){
	//place your code here:
	char *message;
	uint8 i;
	SystemCoreClockUpdate(); /* Get Core Clock Frequency */
	i=pll_init(8000000, LOW_POWER, CRYSTAL, PLL0_PRDIV, PLL0_VDIV, MCGOUT);
	//SysTick_Config(SystemCoreClock/1000);
	if (i!= 0) { while(1);} // Make sure that the PLL is locked on the correct Frequency
	i=what_mcg_mode();
	if (i!= PEE) { while(1);} // Make sure that the PEE mode is enabled
//=============================================================================
	SystemCoreClockUpdate(); // Update the System Core Clock with the new MCG mode
	i=what_mcg_mode();
	if (i!= PEE) { while(1);} // Make sure that the PEE mode is enabled	
//=============================================================================
	uart0_init(UART0_BASE_PTR,48000,TERMINAL_BAUD);
	print("System Configuration done.\n\r");
	cpuInitialization_var= true;// To indicate that this node has been visited
	calculateWCSD2_method();//Calling the next node to be executed
}


void ActivityFinalNode1_method(){
	print("Program ended successfully.\n\r");
}


void calculateRange_method(){
	//place your code here:
	int i=0;
	for (i=0;i<numberOfTrains;i++){
		trainlists[i].range = getWCSD2(trainlists[i])*2 + rangeConst;
	}
	calculateRange_var= true;// To indicate that this node has been visited
	getCurrentSegmentGrade_method();//Calling the next node to be executed
}


void getCurrentSegmentGrade_method(){
	//place your code here:
	int i=0,j=0;
	float currentPos;
	for (i=0;i<numberOfTrains;i++){
		currentPos = trainlists[i].currentPosition;
		for (j=0;j<numberOfSegments;j++){
			if ((currentPos >= segmentList[j].beginLoc) && (currentPos <= segmentList[j].endLoc)){
				trainlists[i].currentSegment = segmentList[j];
				break;
			}
		}
	}
	getCurrentSegmentGrade_var= true;// To indicate that this node has been visited
	getNextStopDistance_method();//Calling the next node to be executed
}


void calculateWCSD2_method(){
	//place your code here:
	while(!strcmp(command,"FINISH") == 0){
		int i=0;
		for (i=0;i<numberOfTrains;i++){
			trainlists[i].wcsd2 = getWCSD2(trainlists[i]);
		}
		calculateWCSD2_var= true;// To indicate that this node has been visited
		calculateRange_method();//Calling the next node to be executed
	}
	ActivityFinalNode1_method();
}


void getNextStopDistance_method(){
	//place your code here:
	int i=0,j=0;
	float minDistToGates = 70000.0,distToNextGate;
	float minDistToTrains = 70000.0,distToNextTrain;
	Gate nextGate;
	Train nextTrain;
	for (i=0;i<numberOfTrains;i++){
		for (j=0;j<numberOfGates;j++){
			distToNextGate = gateList[j].gateDistance - trainlists[i].currentPosition;
			if ((distToNextGate > 0) && (distToNextGate < minDistToGates)){
				nextGate = gateList[j];
				minDistToGates = distToNextGate;
			}
		}
		trainlists[i].nextClosedGate = nextGate;
		minDistToGates = 1000000.0;
	}
	if (numberOfTrains > 1){
		for (i=0;i<numberOfTrains;i++){
			for (j=0;j<numberOfTrains;j++){
				if (i != j){
					distToNextTrain = trainlists[j].currentPosition - trainlists[i].currentPosition;
					if ((distToNextTrain > 0) && (distToNextTrain < minDistToTrains)){
						nextTrain = trainlists[j];
						minDistToTrains = distToNextTrain;
					}
				}
			}
			if (i != j){
				trainlists[i].nextStop = nextTrain.currentPosition;
			}
			minDistToTrains = 1000000.0;
		}
	}else{
		trainlists[0].nextStop = 1000000.0;
	}
	for (i=0;i<numberOfTrains;i++){
		if(trainlists[i].nextStop >= trainlists[i].nextClosedGate.gateDistance){
			trainlists[i].nextStop = trainlists[i].nextClosedGate.gateDistance;
		}
	}
	getNextStopDistance_var= true;// To indicate that this node has been visited
	getCivilSpeed_method();//Calling the next node to be executed
}


void getCivilSpeed_method(){
	//place your code here:
	int i=0,j=0;
	float minCivilSpeed = 100.0;
	Segment nextSegmentInRange;
	for (i=0;i<numberOfTrains;i++){
		nextSegmentInRange = trainlists[i].currentSegment;
		minCivilSpeed = trainlists[i].currentSegment.civilSpeed;
		for (j=0;j<numberOfSegments;j++){
			if ((segmentList[j].beginLoc - trainlists[i].currentPosition) > 0){
				if ((segmentList[j].beginLoc - trainlists[i].currentPosition) < trainlists[i].range){
					if (segmentList[j].civilSpeed < minCivilSpeed){
						nextSegmentInRange = segmentList[j];
					}
				}
			}
		}
		trainlists[i].nextSegmentInRange = nextSegmentInRange;
	}
	if ((trainlists[0].nextStop - trainlists[i].currentPosition) < trainlists[i].range){
		inRange = true;
	}else{
		inRange = false;
	}
	getCivilSpeed_var= true;// To indicate that this node has been visited
	D1_method();//Calling the next node to be executed
}


void D1_method(){
	if( inRange == true ){
		D1_var = true;
		resetCommandedSpeed_method();
	}
	if( inRange == false ){
		D1_var = true;
		updateCommandedSpeed_method();
	}
	D1_var= true;// To indicate that this node has been visited
}// End of Decision node

void resetCommandedSpeed_method(){
	//place your code here:
	trainlists[0].commandedVelocity = 0;
	resetCommandedSpeed_var= true;// To indicate that this node has been visited
	calculateAcmCivilSpeed_method();//Calling the next node to be executed
}


void updateCommandedSpeed_method(){
	//place your code here:
	trainlists[0].commandedVelocity = trainlists[0].nextSegmentInRange.civilSpeed;
	updateCommandedSpeed_var= true;// To indicate that this node has been visited
	calculateAcmCivilSpeed_method();//Calling the next node to be executed
}


void calculateAcmCivilSpeed_method(){
	//place your code here:
	float d1,acc,gradeacc;
	gradeacc = -21.9 * trainlists[0].currentSegment.grade/100.0;
	d1 = trainlists[0].nextSegmentInRange.beginLoc - trainlists[0].currentPosition;
    if (d1 < 0){
        acc = trainlists[0].acceleration + 0.5;
    }else{
        acc = ((pow(trainlists[0].nextSegmentInRange.civilSpeed-2,2) - pow(trainlists[0].velocity,2))/2.0*d1) - gradeacc;
    }

    if ((acc<0) && (acc>-0.45)) {
        acmCivilSpeed = -0.45;
    }else{
        acmCivilSpeed = acc;
    }

	calculateAcmCivilSpeed_var= true;// To indicate that this node has been visited
	calculateAcmNextStop_method();//Calling the next node to be executed
}


void calculateAcmNextStop_method(){
	//place your code here:
	float d2,acc,gradeacc;
	gradeacc = -21.9 * trainlists[0].currentSegment.grade/100.0;
    d2 = trainlists[0].nextStop - trainlists[0].currentPosition - trainlists[0].wcsd2;
    acc = ((-1*pow(trainlists[0].velocity,2))/2.0*d2) - gradeacc;
    if ((trainlists[0].nextStop-trainlists[0].currentPosition) > trainlists[0].range){
        acmNextStop = trainlists[0].acceleration + 0.5;
    }else{
        if ((acc<0 && acc>-0.45) && (d2>((trainlists[0].velocity*deltaTime)+0.5*gradeacc*pow(deltaTime,2)))){
            acmNextStop = 0;
        }else if((acc<0) && (acc>-0.45) && (d2<=((trainlists[0].velocity*deltaTime)+0.5*gradeacc*pow(deltaTime,2)))){
            acmNextStop = -0.45;
        }else{
            acmNextStop = acc;
        }
    }

	calculateAcmNextStop_var= true;// To indicate that this node has been visited
	DecisionNode2_method();//Calling the next node to be executed
}


void DecisionNode2_method(){
	if( acmNextStop <= acmCivilSpeed ){
		DecisionNode2_var = true;
		assignAcmNextStopToAcm_method();
	}
	if( acmCivilSpeed < acmNextStop ){
		DecisionNode2_var = true;
		assignAcmCivilSpeedToAcm_method();
	}
	DecisionNode2_var= true;// To indicate that this node has been visited
}// End of Decision node

void assignAcmNextStopToAcm_method(){
	//place your code here:
	trainlists[0].acm = acmNextStop;
	assignAcmNextStopToAcm_var= true;// To indicate that this node has been visited
	checkAcmBounderies_method();//Calling the next node to be executed
}


void assignAcmCivilSpeedToAcm_method(){
	//place your code here:
	trainlists[0].acm = acmCivilSpeed;
	assignAcmCivilSpeedToAcm_var= true;// To indicate that this node has been visited
	checkAcmBounderies_method();//Calling the next node to be executed
}


void checkAcmBounderies_method(){
	//place your code here:
	float acmNewVal;
    if (trainlists[0].acm < (-2.0)){
    	acmNewVal = -2.0;
    }else if (trainlists[0].acm > 3){
    	acmNewVal = 3;
    }else if (trainlists[0].acm < 0 && (trainlists[0].acm > -0.45)){
    	acmNewVal = -0.45;
    }
    else if (trainlists[0].velocity <= 0.5 && trainlists[0].commandedVelocity == 0){
    	acmNewVal = -2.0;
    }else{
    	acmNewVal = trainlists[0].acm;
    }
    trainlists[0].acm = acmNewVal;
    trainlists[0].commandedAcceleration = trainlists[0].acm;
	checkAcmBounderies_var= true;// To indicate that this node has been visited
	sendNewCommands_method();//Calling the next node to be executed
}


void sendNewCommands_method(){
	//place your code here:
	sendNewCommands_var= true;// To indicate that this node has been visited
	waitToreceiveNewData_method();//Calling the next node to be executed
}


void waitToreceiveNewData_method(){
	//place your code here:

	waitToreceiveNewData_var= true;// To indicate that this node has been visited
	D3_method();//Calling the next node to be executed
}


void D3_method(){
	sprintf(message,"Round %d is done...\n\r",counter++);
	print(message);
	D3_var= true;// To indicate that this node has been visited
}// End of Decision node



