
from tkinter import *
from math import *
import random

####################################
# oop!
####################################

# OBSTACLES

class Obstacle(object):

    def __init__(self, x, y, color):
        self.sidebarWidth = 60
        self.zoom = 3
        self.x = x*self.zoom+self.sidebarWidth
        self.y = y*self.zoom-1200
        self.color = color

    def shift(self, x, y):
        self.x += x
        self.y += y

class ParkBorder(Obstacle):

    def __init__(self):
        self.width = 2550
        self.height = 2000
        self.x = self.width/2
        self.y = self.height/2-1300
        self.color = "black"

    def draw(self, canvas):
        canvas.create_rectangle(self.getCoordinates(),
                                outline=self.color, width=300)

    def getCoordinates(self):
        (left, top, right, bottom) = (self.x-self.width/2, self.y-self.height/2, 
                                      self.x+self.width/2, self.y+self.height/2)
        return (left, top, right, bottom)

    def getBounds(self):
        margin = 170
        (left, top, right, bottom) = (self.x-self.width/2+margin,
                                      self.y-self.height/2+margin, 
                                      self.x+self.width/2-margin, 
                                      self.y+self.height/2-margin)
        return (left, top, right, bottom)

    def personWithinObstacle(self, x, y):
        (left, top, right, bottom) = self.getBounds()
        if (x < left) or (x > right) or (y < top) or (y > bottom):
            return True
        return False

    def createExit(self, canvas):
        (left, top, right, bottom) = self.getCoordinates()
        (cx, cy) = (right-200, top+200)
        (size, color) = (60, "yellow")
        canvas.create_oval(cx-size/2, cy-size/2, cx+size/2, cy+size/2,
                                fill=color, outline="red", width=5)
        canvas.create_text(cx, cy, text="EXIT", font=("Marker Felt", 17))

    def personWithinExit(self, x, y):
        (left, top, right, bottom) = self.getCoordinates()
        (cx, cy) = (right-200, top+200)
        distanceFromCenter = calculateDistance(cx, cy, x, y)
        if distanceFromCenter < 30:
            return True
        return False

class ParkCircle(Obstacle):

    def __init__(self, x, y, r, color):
        super().__init__(x, y, color)
        self.r = r*self.zoom

    def getCoordinates(self):
        (left, top, right, bottom) = (self.x-self.r, self.y-self.r,
                                      self.x+self.r, self.y+self.r)
        return (left, top, right, bottom)

    def draw(self, canvas):
        canvas.create_oval(self.getCoordinates(), width=3, fill=self.color)

    # this function returns True if the point (x, y) is within the obstacle
    def pointWithinObstacle(self, x, y):
        (cx, cy) = (self.x, self.y)
        distanceFromCenter = calculateDistance(cx, cy, x, y)
        if distanceFromCenter < self.r:
            return True
        return False

    def personWithinObstacle(self, x, y):
        (cx, cy) = (self.x, self.y)
        distanceFromCenter = calculateDistance(cx, cy, x, y)
        if distanceFromCenter < self.r+20:
            return True
        return False

class ParkSquare(Obstacle):

    def __init__(self, x, y, size, color):
        super().__init__(x, y, color)
        self.size = size*self.zoom

    def getCoordinates(self):
        (left, top, right, bottom) = (self.x-self.size/2, self.y-self.size/2,
                                      self.x+self.size/2, self.y+self.size/2)
        return (left, top, right, bottom)

    def draw(self, canvas):
        canvas.create_rectangle(self.getCoordinates(), width=3, fill=self.color)

    # this function returns True if the point (x, y) is within the obstacle.
    # (used for bullets)
    def pointWithinObstacle(self, x, y):
        (left, top, right, bottom) = self.getCoordinates()
        if (x < left) or (x > right) or (y < top) or (y > bottom):
            return False
        return True  

    def personWithinObstacle(self, x, y):
        (left, top, right, bottom) = self.getCoordinates()
        if (x < left-20) or (x > right+20) or (y < top-20) or (y > bottom+20):
            return False
        return True 

class ParkRectangle(Obstacle):

    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, color)
        self.width = width*self.zoom
        self.height = height*self.zoom

    def getCoordinates(self):
        (left, top, right, bottom) = (self.x-self.width/2, self.y-self.height/2,
                                      self.x+self.width/2, self.y+self.height/2)
        return (left, top, right, bottom)

    def draw(self, canvas):
        canvas.create_rectangle(self.getCoordinates(), width=3, fill=self.color)

    # this function returns True if the point (x, y) is within the obstacle.
    # (used for bullets)
    def pointWithinObstacle(self, x, y):
        (left, top, right, bottom) = self.getCoordinates()
        if (x < left) or (x > right) or (y < top) or (y > bottom):
            return False
        return True  

    def personWithinObstacle(self, x, y):
        (left, top, right, bottom) = self.getCoordinates()
        if (x < left-20) or (x > right+20) or (y < top-20) or (y > bottom+20):
            return False
        return True 

# PLAYER AND ZOMBIES

class Person(object):

    def __init__(self, x, y):
        self.zoom = 3
        self.x = x*self.zoom
        self.y = y*self.zoom-1200
        self.size = 20
        self.health = 100
        self.sidebarWidth = 60
        self.sidebarColor = "white"

    def draw(self, canvas, data):
        canvas.create_oval(self.x-self.size/2, self.y-self.size/2,
                           self.x+self.size/2, self.y+self.size/2, width=2)

    # this function returns True if a circle (player or zombie) 
    # overlaps another circle (player or zombie).
    def overlap(self, x, y, r):
        (cx, cy, R) = (self.x, self.y, self.size/2)
        distanceBetweenCenters = calculateDistance(cx, cy, x, y)
        if (distanceBetweenCenters < (r+R)):
            return True
        return False

    # returns (cx, cy, r).
    def getLocationAndSize(self):
        return (self.x, self.y, self.size/2)

    def getLocation(self):
        return (self.x, self.y)

class Player(Person):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.weapon = "pistol"

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def decreaseHealth(self):
        self.health -= 8

    def getHealth(self):
        return self.health

    def drawHealth(self, canvas, data):
        (margin, width, height) = (30, 15, 350)
        health = self.health/100
        cx = self.sidebarWidth/2

        if (self.health <= 0): health = 0

        # left side bar:
        canvas.create_rectangle(-10, -10, self.sidebarWidth, data.height+margin, 
                                fill=self.sidebarColor, 
                                outline=self.sidebarColor, width=4)
        # health bar:
        canvas.create_rectangle(cx-width/2, data.height/2-height/2, 
                                cx+width/2, data.height/2+height/2,
                                fill="white", width=2)
        # health level:
        canvas.create_rectangle(cx-width/2, data.height/2+height/2-health*height, 
                                cx+width/2, data.height/2+height/2,
                                fill="pink", outline="pink")
        # health bar border:
        canvas.create_rectangle(cx-width/2, data.height/2-height/2, 
                                cx+width/2, data.height/2+height/2, 
                                width=3)

    def move(self, direction):
        speed = 10
        if (direction == "left"): self.x -= speed
        elif (direction == "right"): self.x += speed
        elif (direction == "up"): self.y -= speed
        elif (direction == "down"): self.y += speed

    def drawWeapon(self, canvas, data):
        (x, y, r) = (self.x, self.y, 25)
        arrowTip   = (x+r*cos(data.theta), y-r*sin(data.theta))
        (arrowHeight, arrowAngle) = (7, 0.4)
        arrowLeft  = (x+(r-arrowHeight)*cos(data.theta+arrowAngle), 
                      y-(r-arrowHeight)*sin(data.theta+arrowAngle))
        arrowRight = (x+(r-arrowHeight)*cos(data.theta-arrowAngle),
                      y-(r-arrowHeight)*sin(data.theta-arrowAngle))
        canvas.create_polygon(arrowTip, arrowLeft, arrowRight, fill="brown")

    def getWeaponPosition(self, data):
        (x, y, r) = (self.x, self.y, 25)
        arrowTip  = (x+r*cos(data.theta), y-r*sin(data.theta))
        return arrowTip

    def drawEquipmentPack(self, canvas, data):
        (margin, size) = (30, 35)
        health = self.health/100
        cx = data.width-self.sidebarWidth/2

        # right side bar:
        canvas.create_rectangle(data.width-self.sidebarWidth, -10, 
                                data.width+10, data.height+10, 
                                fill=self.sidebarColor, 
                                outline=self.sidebarColor, width=4)
        # equipment pack:
        totalHeight = 350
        cy = data.height/2-totalHeight/2+size/2
        totalMargin = totalHeight-(5*size)
        for item in range(5):
            canvas.create_rectangle(cx-size/2, cy-size/2, cx+size/2, cy+size/2,
                                    fill="white", width=3) 
            cy += size+totalMargin/4

class Zombie(Person):
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.eyeY = self.y-3
        self.eyeX = self.x-3.5
        self.eyeSize = 2.8
        self.size = 22
        self.hungry = False

    def draw(self, canvas, data):
        color = "dark blue" if self.hungry == False else "dark red"
        eyeColor = "red" if self.hungry == False else "black"
        canvas.create_oval(self.x-self.size/2, self.y-self.size/2,
                           self.x+self.size/2, self.y+self.size/2,
                           outline=color, fill=color, width=2)
        canvas.create_oval(self.eyeX-self.eyeSize, self.eyeY-self.eyeSize,
                           self.eyeX+self.eyeSize, self.eyeY+self.eyeSize, 
                           fill=eyeColor, outline=eyeColor)
        canvas.create_oval(self.eyeX+7-self.eyeSize, self.eyeY-self.eyeSize,
                           self.eyeX+7+self.eyeSize, self.eyeY+self.eyeSize, 
                           fill=eyeColor, outline=eyeColor)

    def getHealth(self):
        return self.health

    def walk(self, data):
        self.hungry = False

        (x, y) = (0, 0)
        while (x == 0) and (y == 0):
            x = random.choice([-10, 10, 0])
            y = random.choice([-10, 10, 0])

        if (isLegalMove(data, self.x+x, self.y+y) == True):
            self.x += x
            self.y += y
            self.eyeY = self.y-3
            self.eyeX = self.x-3.5

    def shift(self, x, y):
        self.x += x
        self.y += y
        self.eyeY = self.y-3
        self.eyeX = self.x-3.5

    def decreaseHealth(self):
        self.health -= 40

    def chase(self, data):
        self.hungry = True
        (playerX, playerY) = data.player.getLocation()
        (zx, zy) = (self.x, self.y)

        (x, y) = (0, 0)
        while (x == 0) and (y == 0):
            if playerX < zx:
                x = random.choice([0, -10]) 
            elif (playerX >= zx):
                x = random.choice([0, 10]) 
            if playerY < zy:
                y = random.choice([0, -10]) 
            elif (playerY >= zy):
                y = random.choice([0, 10]) 

        if (isLegalMove(data, self.x+x, self.y+y) == True):
            self.x += x
            self.y += y
            self.eyeY = self.y-3
            self.eyeX = self.x-3.5

# BULLET

class Bullet(object):

    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.r = 1
        self.traj = 15 # used to determine line that bullet follows
        self.theta = theta
        self.speed = 20

    def draw(self, canvas, data):
        r = self.traj
        (x, y) = (self.x+r*cos(self.theta), self.y-r*sin(self.theta))
        canvas.create_oval(x-self.r, y-self.r,
                           x+self.r, y+self.r, fill="black")

    def onTimerFired(self, data):
        self.traj += self.speed

    def getPosition(self):
        r = self.traj
        (x, y) = (self.x+r*cos(self.theta), self.y-r*sin(self.theta))
        return (x, y)      

# returns the distance between two points. 
def calculateDistance(cx, cy, x, y):
    return sqrt(((x-cx)**2)+((y-cy)**2))

####################################
# animation!
####################################

def init(canvas, data):
    # logistics:
    (data.cx, data.cy) = (data.width/2, data.height/2)
    data.mode = "splashScreen"
    (data.titleOffset, data.helpTitlePosition) = (40, 1.5/10)
    (data.playButtonCenter, 
     data.helpButtonCenter, 
     data.backButtonCenter) = createButtonCenters(data)
    (data.playButtonCoordinates, 
     data.helpButtonCoordinates, 
     data.backButtonCoordinates) = createButtonCoordinates(data)
    data.backToSplash = True
    data.gameOver = False

    # park:
    (data.smallRide, data.medRide) = (50, 70)
    data.zone1 = createZone1(data)
    data.zone2 = createZone2(data)
    data.zone3 = createZone3(data)
    data.zone4 = createZone4(data)
    data.border = ParkBorder()
    data.park = data.zone1+data.zone2+data.zone3+data.zone4+[data.border]

    # player and zombies:
    data.player = Player(80, data.height-50)
    data.zombies = []
    addZombies(data)
    canvas.data.motionPosn = (data.width/2, data.height/2)
    data.theta = (pi/4)
    data.bullets = []
    data.playerBounds = (200, 150, 650, 450)
    data.screenBounds = (73, data.width-73)
    data.moveZombies = False
    data.lifeStatus = "alive" 
    data.counter = 0

# returns a tuple containing 3 tuples, each corresponding to the rectangle
# coordinates of a play button, help button, and back button.
def createButtonCoordinates(data):
    (halfButtonWidth, halfButtonHeight) = (50, 10)
    (cx, hx, hy) = (data.width/2, halfButtonWidth, halfButtonHeight)
    (splashButtonPosition, backButtonPosition) = (2/3, 3/4)
    (playButtonOffset, backButtonOffset) = (40, 50)

    playButtonCenter = splashButtonPosition*data.height-playButtonOffset
    helpButtonCenter = splashButtonPosition*data.height
    backButtonCenter = backButtonPosition*data.height+backButtonOffset

    # 'rectangle' coordinates of button:
    playButtonCoordinates = (cx-hx, playButtonCenter-hy,
                             cx+hx, playButtonCenter+hy)
    helpButtonCoordinates = (cx-hx, helpButtonCenter-hy,
                             cx+hx, helpButtonCenter+hy)
    backButtonCoordinates = (cx-hx, backButtonCenter-hy,
                             cx+hx, backButtonCenter+hy)

    return (playButtonCoordinates, helpButtonCoordinates, 
            backButtonCoordinates)

# returns a tuple containing the center y coordinates of a 
# play button, help button, and back button.
def createButtonCenters(data):
    (halfButtonWidth, halfButtonHeight) = (50, 10)
    (cx, hx, hy) = (data.width/2, halfButtonWidth, halfButtonHeight)
    (splashButtonPosition, backButtonPosition) = (2/3, 3/4)
    (playButtonOffset, backButtonOffset) = (40, 50)

    playButtonCenter = splashButtonPosition*data.height-playButtonOffset
    helpButtonCenter = splashButtonPosition*data.height
    backButtonCenter = backButtonPosition*data.height+backButtonOffset

    return (playButtonCenter, helpButtonCenter, backButtonCenter)

# DRAWING PARK FUNCTIONS

# creates park obstacles in bottom left section of park.
def createZone1(data):
    result = []
    margin = 60
    # trees:
    (treeX, treeY, treeSize) = (margin, data.height/2-margin-margin/2, 10)
    for tree in range(4):
        result += [ParkCircle(treeX, treeY, treeSize, "dark green")]
        treeY += margin
    # booths:
    (boothX, boothY) = (margin*2, data.height-margin)
    (boothWidth, boothHeight) = (data.smallRide, 20)
    for booth in range(2):
        result += [ParkRectangle(boothX, boothY, boothWidth, boothHeight, 
                                 "orange")]
        boothX += margin+boothHeight/2
    # merry go round:
    (merryX, merryY, merrySize) = (data.width/4, data.height/2, 40)
    result += [ParkCircle(merryX, merryY, merrySize, "dark red")]
    # bottom small ride:
    (rideX, rideY, rideSize) = (margin*3, data.height-margin*3, 50)
    result += [ParkSquare(rideX, rideY, rideSize, "blue")]
    # bottom large ride:
    (rideWidth, rideHeight) = (60, 90)
    result += [ParkRectangle(data.width/2-margin, data.height-margin*2,
                             rideWidth, rideHeight, "red")]
    # circle ride near center:
    result += [ParkCircle(data.width/2-margin, data.height/2+data.smallRide, 
                          25, "coral")]
    return result

# creates park obstacles in top left section of park.
def createZone2(data):
    result = []
    margin = 60
    # top left ride:
    (rideWidth, rideHeight) = (data.smallRide*2, 60)
    (rideX, rideY) = (margin*2, margin)
    result += [ParkRectangle(rideX, rideY, rideWidth, rideHeight, "dark red")]
    # next ride:
    result += [ParkSquare(rideX+margin, rideY+margin*2, margin, "purple")]
    # pair of circle rides:
    (circleX, circleY, r) = (data.width/3, 80, 25)
    result += [ParkCircle(circleX, circleY, r, "coral")]
    result += [ParkCircle(circleX+data.smallRide*2, circleY, r, "coral")]
    # booths:
    (boothX, boothY) = (data.width/2, data.height/3-20)
    (boothHeight, boothWidth) = (data.smallRide, 20)
    for booth in range(2):
        result += [ParkRectangle(boothX, boothY, boothWidth, boothHeight, 
                                 "orange")]
        boothY += margin+boothWidth/2
    boothY = data.height/3-20
    for booth in range(2):
        result += [ParkRectangle(boothX-data.smallRide*2, boothY, 
                                 boothWidth, boothHeight, "orange")]
        boothY += margin+boothWidth/2
    return result

# creates park obstacles in top right section of park.
def createZone3(data):
    result = []
    margin = 60
    # trees:
    (treeX, treeY) = (data.width/2+margin*2, margin)
    (treeMargin, treeSize) = (60, 10)
    for tree in range(4):
        result += [ParkCircle(treeX, treeY, treeSize, "dark green")]
        treeX += treeMargin
    # circle ride at right:
    (x, y, r) = (data.width-margin, data.height/4, 25)
    result += [ParkCircle(x, y, r, "dark red")]
    result += [ParkCircle(x-margin*2, y+margin, r, "red")]
    # med ride:
    (width, height) = (data.medRide, data.smallRide)
    result += [ParkRectangle(x-margin*4-10, y, width, height, "blue")]
    # square ride:
    result += [ParkSquare(data.width/2+margin*2, y+margin*2, 
                          data.smallRide, "purple")]
    return result

# creates park obstacles in bottom right section of park.
def createZone4(data):
    result = []
    margin = 60
    # bottom right ride:
    (rideHeight, rideWidth) = (data.smallRide*2, 60)
    result += [ParkRectangle(data.width-margin, data.height-margin*2, 
                             rideWidth, rideHeight, "purple")]
    # bottom small rides:
    (rideX, rideY, rideSize) = (data.width-margin*3, data.height-margin, 25)
    result += [ParkCircle(rideX, rideY, rideSize, "blue")]
    result += [ParkCircle(rideX-margin, rideY-margin, rideSize, "blue")]
    result += [ParkSquare(rideX-margin*3, rideY, data.smallRide, "coral")]
    # trees:
    (treeX, treeY) = (data.width/2+margin, data.height/2+margin)
    (treeMargin, treeSize) = (80, 10)
    for tree in range(3):
        result += [ParkCircle(treeX, treeY, treeSize, "dark green")]
        treeX += treeMargin
    # large booth:
    (boothX, boothY) = (data.width-margin*(1.5), data.height/2)
    boothSize = 70
    result += [ParkSquare(boothX, boothY, boothSize, "orange")]
    return result

# MAKING ZOMBIES

def addZombies(data):
    while True:
        x = random.randint(70, data.width-70)
        y = random.randint(10, data.height-10)
        if isLegalMove(data, x, y) == True and data.player.overlap(x, y, 30) == False:
            data.zombies += [Zombie(x, y)]
            break

def countZombiesOnScreen(data):
    count = 0 
    (left, top, right, bottom) = data.playerBounds
    left -= 10
    top -= 10
    right += 10
    bottom += 10

    for zombie in data.zombies:
        (x, y, size) = zombie.getLocationAndSize()
        if (x < left) or (x > right) or (y < top) or (y > bottom):
            continue
        count += 1
    return count

####################################
# mode dispatcher
####################################

def mousePressed(event, canvas, data):
    if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
    elif (data.mode == "playGame"):   playGameMousePressed(event, canvas, data)
    elif (data.mode == "help"):       helpMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
    elif (data.mode == "playGame"):   playGameKeyPressed(event, data)
    elif (data.mode == "help"):       helpKeyPressed(event, data)

def timerFired(data):
    if (data.mode == "splashScreen"): splashScreenTimerFired(data)
    elif (data.mode == "playGame"):   playGameTimerFired(data)
    elif (data.mode == "help"):       helpTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
    elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data)
    elif (data.mode == "help"):       helpRedrawAll(canvas, data)

####################################
# splashScreen mode
####################################

def splashScreenMousePressed(event, data):
    if (playGameClicked(event.x, event.y, data) == True):
        data.mode = "playGame"
        data.backToSplash = False # leave splash screen forever
        data.moveZombies = True
    elif (helpClicked(event.x, event.y, data) == True):
        data.mode = "help"
    
# takes in event.x and event.y from mouseclick and returns True if click is
# within 'play game' button coordinates:
def playGameClicked(x, y, data):
    (left, top, right, bottom) = data.playButtonCoordinates
    if ((x >= left) and (x <= right) and (y >= top) and (y <= bottom)):
        return True
    return False

# takes in event.x and event.y from mouseclick and returns True if click is
# within help button coordinates:
def helpClicked(x, y, data):
    (left, top, right, bottom) = data.helpButtonCoordinates
    if ((x >= left) and (x <= right) and (y >= top) and (y <= bottom)):
        return True
    return False

def splashScreenKeyPressed(event, data):
    pass

def splashScreenTimerFired(data):
    pass

def splashScreenRedrawAll(canvas, data):
    # title:
    canvas.create_text(data.width/2, data.height/2-100,
                       text="ZOMBIELAND", font=("Marker Felt", 100),
                       fill="black")
    # new game, current game, help buttons:
    buttonColor = "orange"
    canvas.create_rectangle(data.playButtonCoordinates, outline="white")
    canvas.create_rectangle(data.helpButtonCoordinates, outline="white")
    canvas.create_text(data.width/2, data.playButtonCenter,
                       text="ENTER HERE", font=("Marker Felt", 25),
                       fill=buttonColor)
    canvas.create_text(data.width/2, data.helpButtonCenter,
                       text="RULES", font=("Marker Felt", 25), fill=buttonColor)

####################################
# help mode
####################################

def helpMousePressed(event, data):
    # pressing back button takes you back to whichever screen you came from:
    if ((data.backToSplash == True) and 
        (backClicked(event.x, event.y, data) == True)):
        data.mode = "splashScreen"
    elif ((data.backToSplash == False) and
          (backClicked(event.x, event.y, data) == True)):
        data.mode = "playGame"
        data.moveZombies = True

# takes in event.x and event.y from mouseclick and returns True if click is
# within back button coordinates:
def backClicked(x, y, data):
    (left, top, right, bottom) = data.backButtonCoordinates
    if ((x >= left) and (x <= right) and (y >= top) and (y <= bottom)):
        return True
    return False

def helpKeyPressed(event, data):
    pass

def helpTimerFired(data):
    pass

def helpRedrawAll(canvas, data):
    # title text:
    canvas.create_text(data.width/2, data.height*data.helpTitlePosition, 
                       text="ZOMBIELAND RULES:", font=("Marker Felt", 30),
                       fill="dark red")
    canvas.create_text(data.width/2, data.height*data.helpTitlePosition+45, 
                       text="Get out of Zombieland. Don't get eaten by zombies.", 
                       font=("Marker Felt", 25), fill="dark red")
    # instructions:
    canvas.create_text(data.width/2, data.height/2, 
                       text=helpScreenText(), fill="blue",
                       justify=CENTER, font=("Marker Felt", 20))
    # back button:
    canvas.create_rectangle(data.backButtonCoordinates, outline="white")
    canvas.create_text(data.width/2, data.backButtonCenter, text="BACK",
                       font=("Marker Felt", 24), fill="orange")

# returns a string of help screen instructions.
def helpScreenText():
    text="""



To move, use the arrow keys or "w", "a", "s", "d" keys. Use your cursor to aim your weapon, 
and click to shoot. In case it's not obvious, you should try to aim at the zombies.


Look for the yellow circle labeled "Exit". You're going to want to go to that circle.


Your health is shown on the left, and items you've picked up are shown on the right. 
If your health level decreases to 0, you've died.


Have fun!

"""
    return text


####################################
# playGame mode
####################################

# point weapon:
def mouseMotion(event, data):
    canvas = event.widget.canvas
    canvas.data.motionPosn = (event.x, event.y)
    (x, y) = canvas.data.motionPosn
    # use cursor position to calculate theta = tan-1(y/x)
    distY = data.player.getY()-y
    distX = x-data.player.getX()
    data.theta = atan2(distY, distX)

# fire bullets:
def playGameMousePressed(event, canvas, data):
    if data.gameOver == False:
        (x, y) = data.player.getWeaponPosition(data)
        (theta) = data.theta
        data.bullets += [Bullet(x, y, theta)]

    # when game over:
    elif (playGameClicked(event.x, event.y, data) == True):
        init(canvas, data)       

# this function takes in a point (x, y) and returns False if the point is 
# within any park obstacles.
def isLegalMove(data, x, y):
    for obstacle in data.park:
        if obstacle.personWithinObstacle(x, y) == True:
            return False
    return True

# move player around:
def playGameKeyPressed(event, data):
    (left, top, right, bottom) = data.playerBounds # limit player movement
    (player, overlap) = (data.player, False)
    (x, y, r) = player.getLocationAndSize()

    # go to help screen:
    if (event.keysym == 'h') or (event.char == "?"): 
        data.mode = "help"
        data.moveZombies = False

    # # for demonstration purposes, but not in actual game:
    # elif (event.keysym == 'p'): 
    #     data.moveZombies = not data.moveZombies

    elif (event.keysym == "Up") or (event.keysym == "w"):
        if (isLegalMove(data, x, y-10) == True):
            player.move("up")

            if y < top: # if player exceeds bounds
                player.move("down") # undo player move
                for obstacle in data.park:
                    obstacle.shift(0, 10) # move course instead
                for zombie in data.zombies:
                    zombie.shift(0, 10) # and zombies

            for zombie in data.zombies:
                if zombie.overlap(x, y, r): player.decreaseHealth()


    elif (event.keysym == "Down") or (event.keysym == "s"): 
        if (isLegalMove(data, x, y+10) == True):
            player.move("down")

            if y > bottom: # if player exceeds bounds
                player.move("up") # undo player move
                for obstacle in data.park:
                    obstacle.shift(0, -10) # move course instead
                for zombie in data.zombies:
                    zombie.shift(0, -10) # and zombies

            for zombie in data.zombies:
                if zombie.overlap(x, y, r): player.decreaseHealth()

    elif (event.keysym == "Left") or (event.keysym == "a"): 
        if (isLegalMove(data, x-10, y) == True):
            player.move("left")

            if x < left: # if player exceeds bounds
                player.move("right") # undo player move
                for obstacle in data.park:
                    obstacle.shift(10, 0) # move course instead
                for zombie in data.zombies:
                    zombie.shift(10, 0) # and zombies

            for zombie in data.zombies:
                if zombie.overlap(x, y, r): player.decreaseHealth()


    elif (event.keysym == "Right") or (event.keysym == "d"): 
        if (isLegalMove(data, x+10, y) == True):
            player.move("right")

            if x > right: # if player exceeds bounds
                player.move("left") # undo player move
                for obstacle in data.park:
                    obstacle.shift(-10, 0) # move course instead
                for zombie in data.zombies:
                    zombie.shift(-10, 0) # and zombies

            for zombie in data.zombies:
                if zombie.overlap(x, y, r): player.decreaseHealth()

    if player.getHealth() <= 0:
        data.gameOver = True
        data.lifeStatus = "dead"

    elif data.border.personWithinExit(x, y) == True:
        data.gameOver = True

# bullets and zombies:                
def playGameTimerFired(data):
    data.counter += 1

    # bullets fired:
    for bullet in data.bullets:
        bullet.onTimerFired(data)
        (x, y) = bullet.getPosition()
        if isLegalMove(data, x, y) == False:
            data.bullets.remove(bullet)
        else:
            for zombie in data.zombies:
                if zombie.overlap(x, y, 2) == True: 
                    zombie.decreaseHealth() 
                    if (zombie.getHealth() <= 0): 
                        data.zombies.remove(zombie)
                    data.bullets.remove(bullet)
                    break

    # keep at least 3 zombies on screen:
    if (data.counter%10 == 0) and (countZombiesOnScreen(data) < 3):
        addZombies(data)

    # move zombies around:
    if data.moveZombies == True:
        for zombie in data.zombies:
            (px, py) = data.player.getLocation()
            (zx, zy) = zombie.getLocation()
            distance = calculateDistance(px, py, zx, zy)

            if (distance < data.height/2) and data.counter%2 == 0: 
                zombie.chase(data)

            elif (data.counter%9) == 0 and distance >= data.height/2: 
                zombie.walk(data)

            (x, y, r) = zombie.getLocationAndSize()
            if data.player.overlap(x, y, r+5) == True:
                if data.counter%10 == 0:
                    data.player.decreaseHealth()

    # zombie dead:
    for zombie in data.zombies:
        if (zombie.getHealth() <= 0): 
            data.zombies.remove(zombie)

    # player eaten by zombies:
    if data.player.getHealth() <= 0:
        data.gameOver = True
        data.lifeStatus = "dead"

def playGameRedrawAll(canvas, data):
    if data.gameOver == False:
        drawPark(canvas, data)
        drawZombies(canvas, data)
        drawBullets(canvas, data)
        drawPlayer(canvas, data)
    else:
        drawGameOver(canvas, data)

def drawPlayer(canvas, data):
    data.player.draw(canvas, data)
    data.player.drawHealth(canvas, data)
    data.player.drawWeapon(canvas, data)
    data.player.drawEquipmentPack(canvas, data)

def drawBullets(canvas, data):
    for bullet in data.bullets:
        bullet.draw(canvas, data)

def drawZombies(canvas, data):
    for zombie in data.zombies:
        if (zombie.getHealth() <= 0): 
            data.zombies.remove(zombie)
            continue
        zombie.draw(canvas, data)

def drawPark(canvas, data):
    for obstacle in data.park:
        obstacle.draw(canvas)
    data.border.createExit(canvas)

def drawGameOver(canvas, data):
    if data.lifeStatus == "alive":
        gameOverText = "Congratulations! You've escaped Zombieland."
    elif (data.lifeStatus == "dead"):
        gameOverText = "You died. Way to go."
    textColor = "orange"
    canvas.create_text(data.width/2, data.height/2-50, 
                       text=gameOverText, font=("Marker Felt", 25),)
    canvas.create_rectangle(data.playButtonCoordinates, outline="white")
    canvas.create_text(data.width/2, data.playButtonCenter,
                       text="BACK TO HOME", font=("Marker Felt", 23),
                       fill=textColor)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, canvas, data)
        redrawAllWrapper(canvas, data)

    def mouseMotionWrapper(event, canvas, data):
        mouseMotion(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    canvas.data = Struct()
    init(canvas, data)
    # set up events
    canvas.bind("<Motion>", lambda event:
                            mouseMotionWrapper(event, canvas, data))
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def playZombieland():  
    run(800, 600)

playZombieland()