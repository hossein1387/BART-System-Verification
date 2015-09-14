import math
###########################################################
## Google map python wrapper V0.1
## 
############################################################

class maps:
	instaceCounter = 0
	def __init__(self, centerLat, centerLng, zoom ):
		self.center = (float(centerLat),float(centerLng))
		self.zoom = int(zoom)
		self.grids = None
		self.paths = []
		self.points = []
		self.radpoints = []
		self.trains = []
		self.gridsetting = None
		self.coloricon = 'http://chart.apis.google.com/chart?cht=mm&chs=12x16&chco=FFFFFF,XXXXXX,000000&ext=.png'

	def setgrids(self,slat,elat,latin,slng,elng,lngin):
		self.gridsetting = [slat,elat,latin,slng,elng,lngin]

	def addpoint(self, lat, lng, comment, color = '#FF0000'):
		self.points.append((lat,lng,color[1:],comment))

	#def addpointcoord(self, coord):
	#	self.points.append((coord[0],coord[1]))
	def addTrain(self,latInit,lonInit,trainID):
		self.trains.append((latInit,lonInit,trainID))

	def addradpoint(self, lat,lng,rad,color = '#0000FF'):
		self.radpoints.append((lat,lng,rad,color))

	def addpath(self,pathName,pathCoordinates,pathColor = '#FF0000'):
		path = {'pathName':pathName,'pathColor':pathColor,'pathCoordinates':pathCoordinates}
		self.paths.append(path)
	
	#create the html file which inlcude one google map and all points and paths
	def draw(self, htmlfile):
		f = open(htmlfile,'w')
		f.write('<html>\n')
		f.write('<head>\n')
		f.write('<style>\n')
		f.write('.infoDiv {\n')
		f.write('\theight: 70px; \n')
		f.write('\twidth: 150px;\n')
		f.write('\t-webkit-user-select: none;\n')
		f.write('\tbackground-color: white; \n')
		f.write('\tfont-family:Tahoma;\n')
		f.write('\tfont-size:8pt;\n')
		f.write('\t}\n')
		f.write('</style>\n')
		f.write('<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n')
		f.write('<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>\n')
		f.write('<title>Google Maps - pygmaps </title>\n')
		f.write('<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>\n')
		f.write('<script type="text/javascript">\n')
		f.write('var map;\n')
		f.write('var trainImage;\n')
		self.prototypeTrains(f)
		f.write('\tfunction initialize() {\n')
		self.addImage(f,"default")
		self.drawmap(f)
		self.drawTrains(f)
		self.drawgrids(f)
		self.drawpoints(f)
		self.drawradpoints(f)
		self.drawpaths(f,self.paths)
		f.write('\t}\n')
		self.defineTrainCaller(f)
		f.write('</script>\n')
		f.write('</head>\n')
		f.write('<body style="margin:0px; padding:0px;" onload="initialize()">\n')
		f.write('\t<div id="map_canvas" style="width: 100%; height: 100%;"></div>\n')
		f.write('</body>\n')
		f.write('</html>\n')		
		f.close()

	def drawgrids(self, f):
		if self.gridsetting == None:
			return
		slat = self.gridsetting[0]
		elat = self.gridsetting[1]
		latin = self.gridsetting[2]
		slng = self.gridsetting[3]
		elng = self.gridsetting[4]
		lngin = self.gridsetting[5]
		self.grids = []

		r = [slat+float(x)*latin for x in range(0, int((elat-slat)/latin))]
		for lat in r:
			self.grids.append([(lat+latin/2.0,slng+lngin/2.0),(lat+latin/2.0,elng+lngin/2.0)])

		r = [slng+float(x)*lngin for x in range(0, int((elng-slng)/lngin))]
		for lng in r:
			self.grids.append([(slat+latin/2.0,lng+lngin/2.0),(elat+latin/2.0,lng+lngin/2.0)])
		
		for line in self.grids:
			self.drawPolyline(f,line,strokeColor = "#000000")
	def drawpoints(self,f):
		for point in  self.points:
			self.drawpoint(f,point[0],point[1],point[2],point[3])

	def drawradpoints(self, f):
		for rpoint in self.radpoints:
			path = self.getcycle(rpoint[0:3])
			self.drawPolygon(f,path,strokeColor = rpoint[3])

	def getcycle(self,rpoint):
		cycle = []
		lat = rpoint[0]
		lng = rpoint[1]
		rad = rpoint[2] #unit: meter
		d = (rad/1000.0)/6378.8;
		lat1 = (math.pi/180.0)* lat
		lng1 = (math.pi/180.0)* lng

		r = [x*30 for x in range(12)]
		for a in r:
			tc = (math.pi/180.0)*a;
			y = math.asin(math.sin(lat1)*math.cos(d)+math.cos(lat1)*math.sin(d)*math.cos(tc))
			dlng = math.atan2(math.sin(tc)*math.sin(d)*math.cos(lat1),math.cos(d)-math.sin(lat1)*math.sin(y))
			x = ((lng1-dlng+math.pi) % (2.0*math.pi)) - math.pi 
			cycle.append( ( float(y*(180.0/math.pi)),float(x*(180.0/math.pi)) ) )
		return cycle

	def drawpaths(self, f, paths):
		for path in paths:
			self.drawPolyline(f,path['pathCoordinates'], strokeColor = path['pathColor'])

	def drawTrains(self,f):
		if self.trains:
			for train in self.trains:
				self.createTrains(f,train[0],train[1],train[2])

	def defineTrainCaller(self,f):
		if self.trains:
			for train in self.trains:
				self.trainCaller(f,train[0],train[1],train[2])

	#############################################
	# # # # # # Low level Map Drawing # # # # # # 
	#############################################
	def drawmap(self, f):
		f.write('\t\tvar centerlatlng = new google.maps.LatLng(%f, %f);\n' % (self.center[0],self.center[1]))
		f.write('\t\tvar myOptions = {\n')
		f.write('\t\t\tzoom: %d,\n' % (self.zoom))
		f.write('\t\t\tcenter: centerlatlng,\n')
		f.write('\t\t\tmapTypeId: google.maps.MapTypeId.ROADMAP\n')
		f.write('\t\t};\n')
		f.write('\t\tmap = new google.maps.Map(document.getElementById("map_canvas"), myOptions);\n')
		f.write('\n')



	def drawpoint(self,f,lat,lon,color,comment):
		f.write('\t\tvar latlng = new google.maps.LatLng(%f, %f);\n'%(lat,lon))
		f.write('\t\tvar img = new google.maps.MarkerImage(\'%s\');\n' % (self.coloricon.replace('XXXXXX',color)))
		f.write('\t\tvar marker%d = new google.maps.Marker({\n'%self.instaceCounter)
		f.write('\t\ttitle: "no implimentation",\n')
		f.write('\t\ticon: img,\n')
		f.write('\t\tposition: latlng\n')
		f.write('\t\t});\n')
		f.write('\t\tvar infowindow%d = new google.maps.InfoWindow({\n'%self.instaceCounter)
		if comment == 'default':
			f.write('\t\t\tcontent: "<div class=\'infoDiv\'><h4>BART Simulator</h4>Latitude: %f <br/> Longtitude: %f</div>"\n'%(lat,lon))
		else:
			f.write('\t\t\tcontent: "<div class=\'infoDiv\'><h4>%s</h4>Latitude: %f <br/> Longtitude: %f</div>"\n'%(comment,lat,lon))			
		f.write('\t\t});\n')
		f.write('\t\tgoogle.maps.event.addListener(marker%d, \'click\', function () {\n'%self.instaceCounter)
		f.write('\t\t\tinfowindow%d.open(map, marker%d);\n'%(self.instaceCounter,self.instaceCounter))
		f.write('\t\t});\n')
		f.write('\t\tmarker%d.setMap(map);\n'%self.instaceCounter)
		f.write('\n\n\n')   
		self.instaceCounter+=1                
     
                           		
	def drawPolyline(self,f,path,\
			clickable = False, \
			strokeColor = "#FF0000",\
			strokeOpacity = 1.0,\
			strokeWeight = 2
			):
		f.write('var PolylineCoordinates = [\n')
		for coordinate in path:
			f.write('new google.maps.LatLng(%f, %f),\n' % (coordinate[0],coordinate[1]))
		f.write('];\n')
		f.write('\n')
		f.write('var Path = new google.maps.Polyline({\n')
		f.write('clickable: %s,\n' % (str(clickable).lower()))
		f.write('path: PolylineCoordinates,\n')
		f.write('strokeColor: "%s",\n' %(strokeColor))
		f.write('strokeOpacity: %f,\n' % (strokeOpacity))
		f.write('strokeWeight: %d\n' % (strokeWeight))
		f.write('});\n')
		f.write('\n')
		f.write('Path.setMap(map);\n')
		f.write('\n\n')

	def drawPolygon(self,f,path,\
			clickable = False, \
			fillColor = "#000000",\
			fillOpacity = 0.0,\
			strokeColor = "#FF0000",\
			strokeOpacity = 1.0,\
			strokeWeight = 1
			):
		f.write('var coords = [\n')
		for coordinate in path:
			f.write('new google.maps.LatLng(%f, %f),\n' % (coordinate[0],coordinate[1]))
		f.write('];\n')
		f.write('\n')

		f.write('var polygon = new google.maps.Polygon({\n')
		f.write('clickable: %s,\n' % (str(clickable).lower()))
		f.write('fillColor: "%s",\n' %(fillColor))
		f.write('fillOpacity: %f,\n' % (fillOpacity))
		f.write('paths: coords,\n')
		f.write('strokeColor: "%s",\n' %(strokeColor))
		f.write('strokeOpacity: %f,\n' % (strokeOpacity))
		f.write('strokeWeight: %d\n' % (strokeWeight))
		f.write('});\n')
		f.write('\n')
		f.write('polygon.setMap(map);\n')
		f.write('\n\n')

	def createTrains(self,f,initLat,initLon,trainID):
		f.write('\t trainMarker%d = new google.maps.Marker({\n'%trainID)
		f.write('\t\'position\': new google.maps.LatLng(\'%f\', \'%f\'),\n'%(initLat,initLon))
		f.write('\t\'map\': map,\n')
		f.write('\ticon: trainImage,\n')
		f.write('\'title\': \"Title\"\n')
		f.write('\t});\n')
		f.write('\t trainInfoWindow%d = new google.maps.InfoWindow({\n'%trainID)
		f.write('\t\tcontent: "<div class=\'infoDiv\'><h4>Train Position:</h4>Latitude: N/A <br/> Longtitude: N/A</div>"\n')
		f.write('\t});\n')
		f.write('\tgoogle.maps.event.addListener(trainMarker%d, \'click\', function () {\n'%trainID)
		f.write('\ttrainInfoWindow%d.open(map, trainMarker%d);\n'%(trainID,trainID))
		f.write('\t});\n')

	def trainCaller(self,f,initLat,initLon,trainID):
		f.write('var la%d=\'%f\';\n'%(trainID,initLat))
		f.write('var lo%d=\'%f\';\n'%(trainID,initLon))
		f.write('setInterval(function(){update()},300);\n')
		f.write('function ReadLon(file){\n')
		f.write('\tvar rawFile = new XMLHttpRequest();\n')
		f.write('\trawFile.open("GET", file, false);\n')
		f.write('\trawFile.onreadystatechange = function ()\n')
		f.write('\t{\n')
		f.write('\tif(rawFile.readyState === 4)\n')
		f.write('\t\t{\n')
		f.write('\t\t\tif(rawFile.status === 200 || rawFile.status == 0)\n')
		f.write('\t\t\t{\n')
		f.write('\t\t\t\tvar allText = rawFile.responseText;\n')
		f.write('\t\t\t\tlo%d = allText;\n'%trainID)
		f.write('\t\t\t}\n')
		f.write('\t\t}\n')
		f.write('\t}\n')
		f.write('\trawFile.send(null);\n')
		f.write('}\n')
		f.write('function ReadLat(file){\n')
		f.write('\tvar rawFile = new XMLHttpRequest();\n')
		f.write('\trawFile.open("GET", file, false);\n')
		f.write('\trawFile.onreadystatechange = function ()\n')
		f.write('\t{\n')
		f.write('\tif(rawFile.readyState === 4)\n')
		f.write('\t\t{\n')
		f.write('\t\t\tif(rawFile.status === 200 || rawFile.status == 0)\n')
		f.write('\t\t\t{\n')
		f.write('\t\t\t\tvar allText = rawFile.responseText;\n')
		f.write('\t\t\tla%d = allText;\n'%trainID)
		f.write('\t\t\t}\n')
		f.write('\t\t}\n')
		f.write('\t}\n')
		f.write('\trawFile.send(null);\n')
		f.write('}\n')
		f.write('function makeMarker(){\n')
		f.write('\tposition = new google.maps.LatLng(la%d,lo%d);\n'%(trainID,trainID))
		f.write('\tcenter = new google.maps.LatLng(la%d, lo%d);\n'%(trainID,trainID))
		f.write('\ttrainMarker%d.setPosition(position);\n'%trainID)
		f.write('\tmap.setCenter(center);\n')
		f.write('\tvar contentStr = "<div class=\'infoDiv\'><h4>Train Position:</h4>Latitude:";\n')
		f.write('\tcontentStr = contentStr.concat(la%d);\n'%trainID)
		f.write('\tcontentStr = contentStr.concat("<br/> Longtitude:");\n')
		f.write('\tcontentStr = contentStr.concat(lo%d);\n'%trainID)
		f.write('\tcontentStr = contentStr.concat("</div>");\n')
		f.write('\ttrainInfoWindow%d.setContent(contentStr);\n'%trainID)
		f.write('}\n')
		f.write('function update(){\n')
		f.write('\tmakeMarker();\n')
		f.write('\tReadLat("file:///Users/Hossein/Dropbox/My Works/CODES/Python/BART_Simulator/LAT_COOR_%d.dat");\n'%trainID)
		f.write('\tReadLon("file:///Users/Hossein/Dropbox/My Works/CODES/Python/BART_Simulator/LON_COOR_%d.dat");\n'%trainID)
		f.write('}\n')

	def prototypeTrains(self,f):
		for train in self.trains:
			f.write('var trainMarker%d;\n'%train[2])
			f.write('var trainInfoWindow%d;\n'%train[2])

	def addImage(self,f,imagePath):
		if imagePath == "default":
			f.write('\tvar trainImage = new google.maps.MarkerImage(\'/Users/Hossein/Dropbox/steamtrain.png\');\n')
		else:
			f.write('\tvar trainImage = new google.maps.MarkerImage(\'%s\');\n'%(imagePath))
