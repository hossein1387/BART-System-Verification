//--------------------------------------------------------------------------------
// Company: Concordia University
// Author : MohammadHossein Askari-Hemmat
// Design Name: BART system simulator
// Date: 12.29.2014
// Compiler Versions: Python 2.7
// Version: 1.0
//--------------------------------------------------------------------------------
Bay Area Rapid Transit (BART) is a rapid transit system serving the San Francisco 
Bay Area. The heavy-rail public transit and subway system connects San Francisco 
with cities in the East Bay and suburbs in northern San Mateo County. BART's rapid
transit system operates five routes on 104 miles (167 km) of line, with 44 stations 
in four counties. BART is operated by the San Francisco Bay Area Rapid Transit 
District, a special-purpose transit district that was formed in 1957 to cover 
San Francisco, Alameda County, and Contra Costa County.
In this project a small scale version of BART was under study. We used the control
algorithm which were propoed in "Formal Methods For Embedded Distributed Systems" by
Fabrice Kordon and Michel Lemoine. For more information regarding the book and the 
BART system please refer to the following links:
	[1] http://en.wikipedia.org/wiki/Bay_Area_Rapid_Transit
	[2] http://www.bart.gov/
	[3] http://www.springer.com/computer/theoretical+computer+science/book/978-1-4020-7996-2

The propose of this project is to show the features of the developed tool for rapid
prototyping. This case study is consist of three main parts:
	1- A UML Activity diagrams which represents the high level behavior of the Station Computer
	   in BART system
	2- A Model to code generator which automatically converts the high level model,
	   represented in UML, to the low level C/C++ code ready to be implemented on a target 
	   platform.
	3- A python script which will simulate trains, gates, segments in the BART system
The main task in this case study is to implement a control algorithm to control the speed and 
acceleration of trains in a way that meet the following constraint:
	1- A train does not hit a train in front of it
	2- A train does not enter a closed gate
	3- A train does not reach the limited Speed of it's current track(segment)
In our approach, first, we defined the control algorithm in UML. Then, by using the developed
tool, the implementation code was generated and the target platform was programmed with the 
model. In order to verify the correct behavior of the system, other parts of the BART system 
was defined in Python. The target platform was then connected to the PC so that the BART Station 
Computer could send its command to the rest of the system. The following files were written to 
simulate the behavior of the BART system:
	1-BART.py	
	2-Gate.py
	3-Segment.py
	4-StationComputer.py
	5-Train.py
	6-utility.py
To simplify the model, only one track in BART was targeted. Here are the segments and gates with 
their corresponding distances from the begining od th etrack:

//--------------------------------------------------------------------------------
Segments:
//--------------------------------------------------------------------------------
Segment: DUBL_CAST_E starts at 0km and ends in 16.0001978529km ---> Segment length:16000.1978529
Segment: CAST_E_BAYF_S starts at 16.0001978529km and ends in 19.7048957742km ---> Segment length:3704.69792135
Segment: OAKY_BAYF_S starts at 19.7048957742km and ends in 38.1585092467km ---> Segment length:18453.6134725
Segment: OAKY_SE starts at 38.1585092467km and ends in 38.7491571804km ---> Segment length:590.647933648
Segment: OAKY_DALY starts at 38.7491571804km and ends in 62.6906771109km ---> Segment length:23941.5199305

//--------------------------------------------------------------------------------
Gates:
//--------------------------------------------------------------------------------
Gate '16th St. Mission (16TH)' is located at 53932.1990199 is Open
Gate '24th St. Mission (24TH)' is located at 55350.1604208 is Open
Gate 'Balboa Park (BALB)' is located at 59855.1209469 is Open
Gate 'Bay Fair (BAYF)' is located at 21396.1761693 is Open
Gate 'Castro Valley (CAST)' is located at 16129.5900042 is Open
Gate 'Civic Center/UN Plaza (CIVC)' is located at 52306.3549054 is Open
Gate 'Coliseum/Oakland Airport (COLS)' is located at 30028.609238 is Open
Gate 'Daly City (DALY)' is located at 62690.6771109 is Open
Gate 'Dublin/Pleasanton (DUBL)' is located at 27.6581521603 is Open
Gate 'Embarcadero (EMBR)' is located at 50023.7818701 is Open
Gate 'Fruitvale (FTVL)' is located at 33273.5628714 is Open
Gate 'Glen Park (GLEN)' is located at 58038.2806387 is Open
Gate 'Lake Merritt (LAKE)' is located at 37714.1837826 is Open
Gate 'Montgomery St. (MONT)' is located at 50577.6855601 is Open
Gate 'Powell St. (POWL)' is located at 51441.5310924 is Open
Gate 'San Leandro (SANL)' is located at 25428.4265761 is Open
Gate 'West Dublin/Pleasanton (WDUB)' is located at 2697.67168648 is Open
Gate 'West Oakland (WOAK)' is located at 40577.9900176 is Open

All gates are considered to be opened. As a result, train can pass all the gates without taking full stop. This
assumption was mandatory to allow back to back simulation. 
