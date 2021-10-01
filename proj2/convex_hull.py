from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
  from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
  from PyQt4.QtCore import QLineF, QPointF, QObject
else:
  raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25

LEFTMOST_PT_IDX = 0 # In hulls created, leftmost points will be index 0

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

  # Class constructor
  def __init__( self):
    super().__init__()
    self.pause = False
    
# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

  def showTangent(self, line, color):
    self.view.addLines(line,color)
    if self.pause:
      time.sleep(PAUSE)

  def eraseTangent(self, line):
    self.view.clearLines(line)

  def blinkTangent(self,line,color):
    self.showTangent(line,color)
    self.eraseTangent(line)

  def showHull(self, polygon, color):
    self.view.addLines(polygon,color)
    if self.pause:
      time.sleep(PAUSE)
    
  def eraseHull(self,polygon):
    self.view.clearLines(polygon)
    
  def showText(self,text):
    self.view.displayStatusText(text)
  

# This is the method that gets called by the GUI and actually executes
# the finding of the hull
  def compute_hull(self, points, pause, view):
    self.pause = pause
    self.view = view

    assert(type(points) == list and type(points[0]) == QPointF)

    # Sorts the points by increasing x-value
    points.sort(key= lambda k: k.x())	# Overwrites points with same but new order

    t3 = time.time()
    polygonPts = self.solve(points)
    polygon = self.toPolygon(polygonPts)
    t4 = time.time()

    self.showTangent(polygon, BLUE);

    # when passing ines to the display, pass a list of QLineF objects.  Each QLineF
    # object can be created with two QPointF objects corresponding to the endpoints
    self.showHull(polygon,RED)
    self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))

    polygon = []

  '''Divide-and-conquer convex hull solver (recursive)'''
  def solve(self, points):
    # Base case
    if len(points) <= 2:  # If 2 points, have array with 1 line connecting the 2 points
      return points

    # Recursive case
    midIdx = len(points) // 2
    leftHull = self.solve(points[:midIdx])	# First half
    rightHull = self.solve(points[midIdx:])	# Second half
    return self.combine(leftHull, rightHull)
  
  '''Converts array of QPointF points to an array of QLineF lines'''
  def toPolygon(self, points):                                            # O(n)    
    polygon = []
    for i in range(len(points)):                                          # O(n)
      if i < len(points) - 1:
        polygon.append(QLineF(self.at(points, i), self.at(points, i+1)))
      else:   # On last iteration connect last point to first
        polygon.append(QLineF(self.at(points, i), self.at(points, 0)))
    return polygon

  '''
  NOTE
  Hulls are sorted in cw order
  The 1st element in a hull is its leftmost point
  '''

  '''Finds upper/lower tangent of each hull, then returns back indices for the left and right 2 upper/lower tangents.'''
  def findTangentIndices(self, leftHull, rightHull, findLower):
    # Find rightmost point of left hullleftmost and rightmost points
    leftCurrIndex = self.getRightmostPtIdx(leftHull)
    rightCurrIdx = LEFTMOST_PT_IDX

    fullyOptimized = False

    while not fullyOptimized:
      fullyOptimized = True

      # Left Side - finding optimal point
      
      leftNextIdx = leftCurrIndex - 1 # Left hull's next counter-clockwise index
      if findLower:
        leftNextIdx = leftCurrIndex + 1 # Left hull's next clockwise index

      currSlope = self.findSlope(self.at(rightHull, rightCurrIdx), self.at(leftHull, leftCurrIndex))
      nextSlope = self.findSlope(self.at(rightHull, rightCurrIdx), self.at(leftHull, leftNextIdx))

      isBetter = nextSlope < currSlope
      if findLower:
        isBetter = nextSlope > currSlope

      if isBetter:
        currSlope = nextSlope
        leftCurrIndex = leftNextIdx
        fullyOptimized = False

      # Right Side - finding optimal point

      rightNextIdx = rightCurrIdx + 1  # Right hull's next clockwise index
      if findLower:
        rightNextIdx = rightCurrIdx - 1 # Right hull's next counter-clockwise index
      
      currSlope = self.findSlope(self.at(leftHull, leftCurrIndex), self.at(rightHull, rightCurrIdx))
      nextSlope = self.findSlope(self.at(leftHull, leftCurrIndex), self.at(rightHull, rightNextIdx))

      isBetter = nextSlope > currSlope
      if findLower:
        isBetter = nextSlope < currSlope

      if isBetter:
        currSlope = nextSlope
        rightCurrIdx = rightNextIdx
        fullyOptimized = False
      
    return leftCurrIndex % len(leftHull), rightCurrIdx % len(rightHull) # Adjusts indices to be within array

  '''Combines 2 hulls together (returns a list of lines)'''
  def combine(self, leftHull, rightHull):
    # Find upper tangent connecting the hulls
    leftUpperIdx, rightUpperIdx = self.findTangentIndices(leftHull, rightHull, False)
    # Find lower tangent connecting the hulls
    leftLowerIdx, rightLowerIdx = self.findTangentIndices(leftHull, rightHull, True)
    
    # Combine points together into new hull
    comboHull = []
    comboHull = self.addPoints(comboHull, leftHull, 0, leftUpperIdx) # Top part of left hull to keep
    comboHull = self.addPoints(comboHull, rightHull, rightUpperIdx, rightLowerIdx) # Part of right hull to keep
    comboHull = self.addLowerLeftPoints(comboHull, leftHull, leftLowerIdx) # Bottom part of left hull to keep

    return comboHull

  '''Finds slope of the line made by connecting the 2 points passed in'''
  def findSlope(self, point1, point2):
    line = QLineF(point1, point2)
    return line.dy() / line.dx()

  '''Returns index of item in hull (handles logic so that hull can loop circularly).'''
  def at(self, hull, index):
    return hull[index % len(hull)]

  '''Adds points from an old hull to a new one'''
  def addPoints(self, newHull, oldHull, currIdx, finalIdx):
    newHull.append(self.at(oldHull, currIdx))
    while (currIdx % len(oldHull)) != (finalIdx % len(oldHull)):
        currIdx += 1
        newHull.append(self.at(oldHull, currIdx % len(oldHull)))

    return newHull

  '''Handles edge case for adding points to the lower left of a hull'''
  def addLowerLeftPoints(self, newHull, leftHull, leftLowerIdx):
    if len(leftHull) == 1:
      return newHull

    while (leftLowerIdx % len(leftHull)) != 0:
      newHull.append(self.at(leftHull, leftLowerIdx))
      leftLowerIdx += 1
    return newHull

  '''Returns the index of the rightmost point in hull'''
  def getRightmostPtIdx(self, hull):
    biggestXVal = max(hull, key= lambda k: k.x())
    return hull.index(biggestXVal)