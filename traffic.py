import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation
import sys

#details of traffic issues, user edits
slowlane = 1
slowspeed = 10

#initialize lanes
time = np.arange(1,100,1)
lane0 = [1000,6]
lane1 = [1000,6]
lane2 = [1000,6]
lane3 = [1000,6]
traffic = [lane0,lane1,lane2,lane3]

lanedict0 = [{'location':lane0[0],'lane':0,'lanefin':0},{'location':lane0[1],'lane':0,'lanefin':0}]
lanedict1 = [{'location':lane1[0],'lane':1,'lanefin':1},{'location':lane1[1],'lane':1,'lanefin':1}]
lanedict2 = [{'location':lane2[0],'lane':2,'lanefin':2},{'location':lane2[1],'lane':2,'lanefin':2}]
lanedict3 = [{'location':lane3[0],'lane':3,'lanefin':3},{'location':lane3[1],'lane':3,'lanefin':3}]
trafficdict = [lanedict0,lanedict1,lanedict2,lanedict3]

#initialize plot
x = np.linspace(0, 10000,2)
y = np.linspace(0,3,2)
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line0, = ax.plot(x, y, 'ro')
line1, = ax.plot(x, y, 'bo')
line2, = ax.plot(x, y, 'go')
line3, = ax.plot(x, y, 'yo')

def addcar(lane,lanedict):
    carplotcount = 0
    lanecurcarlocs = list(object['location'] for object in lanedict) #list of cars location in current lane
    if min(lanecurcarlocs) > 300:   #if there is no car with a location under 300 add a car to this lane
        lanestart = lanedict[0]['lane']
        lanedict.append({'location':0,'lane':lanestart,'lanefin':lanestart})

def acceleration(lane,lanedict):

    carcount = 0
    lanecurcarlocs = list(object['location'] for object in lanedict) #list of cars location in current lane

    #can impose conditions on the lead car's speed
    leadspeed = 60
    if lanedict[0]['lane'] == 3:
        leadspeed = 80
    if lanedict[0]['lane'] == slowlane:
        leadspeed = slowspeed

    for car in lanedict:  #speed based on distance to next car
        if carcount == 0:
            car['location'] += leadspeed #first car in each lane goes 'speedlimit'
        else:   #else if close to next car move a fraction of the distance, if far - floor it
            carlocation = car['location'] 
            nextcar = min([i for i in lanecurcarlocs if i > carlocation])
            if nextcar - carlocation < 500: #else if close to next car move a fraction of the distance
                car['location'] += round(.10*(nextcar - carlocation),0)
            else: #if far - floor it
                car['location'] += 90
        carcount += 1
                
            
blockedlane = 1
lanechangerdown = 10000
#loop through time and define switching lanes conditions
for phase in range(len(time)):
    addcar(lane0,lanedict0)
    addcar(lane1,lanedict1)
    addcar(lane2,lanedict2)
    addcar(lane3,lanedict3)
    
    acceleration(lane0,lanedict0)
    acceleration(lane1,lanedict1)
    acceleration(lane2,lanedict2)
    acceleration(lane3,lanedict3)
    traffic = [lane0,lane1,lane2,lane3]
    
    lanenumber = 0
    position = 0
    positionlast = 0
    frontspace = 250
    backspace = 30
    carspace = 200
    for lanedict in trafficdict:
        carcount = 0        
        for car in lanedict: #switching lanes up
 ##           print(car)
            carlocation  = car['location'] #current car location
            lanecurcarlocs = list(object['location'] for object in trafficdict[lanenumber]) #list of cars location in current lane
            if lanenumber != 3 and lanenumber + 1!= blockedlane and carlocation != max(lanecurcarlocs): #cars in last lane cant go up anymore
                laneupcarlocs = list(object['location'] for object in trafficdict[lanenumber+1]) #list of cars location in lane up
                if carlocation < max(laneupcarlocs): #make sure not switching lanes ahead of front car of next lane
                  #print(car)
                  lanechangerup = 10000
                  #make sure there is space in the next lane up
                  #make sure there is more space in next lane than current one
                  #make sure no other cars just switched lanes nearby (lanechangerup/down)
                  if all(carloc <= carlocation - backspace or carloc > carlocation + frontspace for carloc in laneupcarlocs) \
                     and min([i for i in laneupcarlocs if i > carlocation]) > min([i for i in lanecurcarlocs if i > carlocation])\
                     and all(carloc <= lanechangerdown - carspace or carloc > lanechangerdown + carspace for carloc in lanecurcarlocs):  
                      carlocation  = car['location']
                      lanechangerup = carlocation
                      print(car,'up',lanechangerdown)
##                      print(lanecurcarlocs,'current lane')
##                      print(laneupcarlocs,'lane up')
                      #sys.exit()
                      trafficdict[lanenumber+1].insert(-1,trafficdict[lanenumber][carcount])
                      trafficdict[lanenumber].pop(carcount)
                      lanechangerdown = 10000  
                      break
            if lanenumber != 0 and lanenumber -1 != blockedlane and carlocation != max(lanecurcarlocs): #lane conditions for switching down, mirror switching up conditions
                lanedowncarlocs = list(object['location'] for object in trafficdict[lanenumber-1]) #list of cars location in lane down
                if carlocation < max(lanedowncarlocs):
                  #print(car)
                  if all(carloc <= carlocation - backspace or carloc > carlocation + frontspace for carloc in lanedowncarlocs) \
                     and min([i for i in lanedowncarlocs if i > carlocation]) > min([i for i in lanecurcarlocs if i > carlocation])\
                     and all(carloc <= lanechangerup - carspace or carloc > lanechangerup + carspace for carloc in lanecurcarlocs):
                      carlocation  = car['location']
                      lanechangerdown = carlocation                    
##                      print(car,trafficdict[lanenumber][carcount],'down')
##                      print(lanecurcarlocs,'current lane')
##                      print(lanedowncarlocs,'lane down')
                      #sys.exit()
                      print(car,'dwon',lanechangerdown)
                      trafficdict[lanenumber-1].insert(-1,trafficdict[lanenumber][carcount])
                      trafficdict[lanenumber].pop(carcount)
                      break
            carcount += 1
        lanenumber += 1
        print(lanenumber)
       
    lane00 = []
    lane11 = []
    lane22 = []
    lane33 = []
    lane = 0
    for lanedict in trafficdict:
        for car in lanedict:
            lanestart = car['lane']
            if lanestart == 0:
                car['lanefin'] = lane
                lane00.append(car)

            if lanestart == 1:
                car['lanefin'] = lane
                lane11.append(car)

            if lanestart == 2:
                car['lanefin'] = lane

                lane22.append(car)
            if lanestart == 3:
                car['lanefin'] = lane
                lane33.append(car)
        lane += 1
                    
    lane0x = list((object['location'] for object in lane00))
    lane0y = list((object['lanefin'] for object in lane00))
    lane1x = list((object['location'] for object in lane11))
    lane1y = list((object['lanefin'] for object in lane11))
    lane2x = list((object['location'] for object in lane22))
    lane2y = list((object['lanefin'] for object in lane22)) 
    lane3x = list((object['location'] for object in lane33))
    lane3y = list((object['lanefin'] for object in lane33))

    line0.set_xdata(lane0x)
    line0.set_ydata(lane0y)
    line1.set_xdata(lane1x)
    line1.set_ydata(lane1y)
    line2.set_xdata(lane2x)
    line2.set_ydata(lane2y)
    line3.set_xdata(lane3x)
    line3.set_ydata(lane3y)
##
##    line1.set_xdata(lane1)
##    line1.set_ydata(np.ones(len(lane1)))
##    line2.set_xdata(lane2)
##    line2.set_ydata(np.ones(len(lane2))*2)
##    line3.set_xdata(lane3)
##    line3.set_ydata(np.ones(len(lane3))*3)
##    line4.set_xdata(lane4)
##    line4.set_ydata(np.ones(len(lane4))*4)

    fig.canvas.draw()
    plt.pause(0.01)
