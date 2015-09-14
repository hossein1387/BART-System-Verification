def parser():
    KMLFilePath = '/Users/Hossein/Downloads/bart.kml'
    KMLFile = open(KMLFilePath)
    convertedTextFile = open('BART_COOR.dat', 'wb')
    data = KMLFile.read()
    tree = ET.parse(KMLFilePath) 
    lineStrings = tree.findall('.//{http://www.opengis.net/kml/2.2}LineString')
    coordinationsStr = ''
    RouteCoordinationsList = []
    RouteXCoordinationsList = []
    RouteYCoordinationsList = []
    coordinationsStr = ""
    xCounter = 0
    yCounter = 0
    doc  = parse('/Users/Hossein/Downloads/bart.kml')
    for folders in doc.findall('.//{http://www.opengis.net/kml/2.2}Folder'):
        for places in folders.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
            placeName =  places.findtext('.//{http://www.opengis.net/kml/2.2}name')
            if placeName == 'DUBL-DALY (ROUTE 11/12)':
                for geometry in places.findall('.//{http://www.opengis.net/kml/2.2}MultiGeometry'):
                    for linestring in geometry.findall('.//{http://www.opengis.net/kml/2.2}LineString'):
                        for coor in geometry.findall('.//{http://www.opengis.net/kml/2.2}coordinates'):
                            coordinationsStr += coor.text
#                            print placeName
    #print coordinationsStr             
    if coordinationsStr == " ":
        print "No correct coordination was found in:" + KMLFilePath
    else:
        convertedTextFile.write(coordinationsStr)
        convertedTextFile.close()
        num1 = ""
        num2 = ""
        newNumber1 = True
        newNumber2 = False
        for chr in coordinationsStr:
            if (xCounter<12273):
                if newNumber1:
                    if not(chr == ",") and not(chr == " "):
                        num1+=chr
                        continue
                    elif (chr == ","):
                        newNumber2 = True
                        newNumber1 = False
                        
                        data = round(float(num1),4)
                        RouteXCoordinationsList.append(data)
                        xCounter+=1
                        num1 = ""
                        continue
                if newNumber2:
                    if not(chr == " "):
                        num2+=chr
                        continue
                    else:
                        data = round(float(num2),4)
                        RouteYCoordinationsList.append(data)
                        yCounter+=1
                        num2 = ""
                        newNumber2 = False
                        newNumber1 = True
                        continue
                    
        for index,item in enumerate(RouteYCoordinationsList):
#            RouteCoordinationsList.append(LatLonToXY(RouteXCoordinationsList[index],RouteYCoordinationsList[index]))
            RouteCoordinationsList.append((RouteYCoordinationsList[index],RouteXCoordinationsList[index]))
        return RouteCoordinationsList




def addPoint(point):
    global templateFile
    targetFile = open(templateFile,'r+')
    tempString = ""
    pointStr = '\n\t\t\tvar marker = new google.maps.Marker({\n \t\t\t\t\t\t\t\t\'position\': new google.maps.LatLng(\''+str(point[0])+'\',\''+str(point[1])+'\'),\n\t\t\t\t\t\t\t\t\'map\': map,\n\t\t\t\t\t\t\t\t\'title\': "Title"});\n'    
    tempString = headerTxt + pointStr + endingTxt              
    targetFile.close()
    open(templateFile, 'w').close()
    targetFile = open(templateFile,'w')
    targetFile.write(tempString)
    targetFile.close()
