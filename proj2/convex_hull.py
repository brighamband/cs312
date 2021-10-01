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
  def compute_hull(self, points, pause, view):                                          # Fn - T O(nlogn) | S(n)
    self.pause = pause
    self.view = view

    assert(type(points) == list and type(points[0]) == QPointF)

    # Sorts the points by increasing x-value
    points.sort(key= lambda k: k.x())	# Overwrites points with same but new order       # T O(nlogn) - Sorting optimized by Python

    t3 = time.time()                                                                    # S O(1)
    polygonPts = self.solve(points)                                                     # n*logn | S O(n) - See fn, 1 array
    polygon = self.toPolygon(polygonPts)                                                # T O(n) | S O(1) - See fn
    t4 = time.time()                                                                    # S O(1)

    self.showTangent(polygon, BLUE);

    # when passing ines to the display, pass a list of QLineF objects.  Each QLineF
    # object can be created with two QPointF objects corresponding to the endpoints
    self.showHull(polygon,RED)
    self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))

    polygon = []

  '''Divide-and-conquer convex hull solver (recursive)'''
  def solve(self, points):                                                                  # T n*logn | S O(n) - Technically S 3n
    # Base case
    if len(points) <= 2:  # If 2 points, have array with 1 line connecting the 2 points
      return points

    # Recursive case
    midIdx = len(points) // 2                                                               # O(1) - Big O of n, not N
    leftHull = self.solve(points[:midIdx])	# First half                                    # T O(logn) | S O(n) - 1 array, recursve
    rightHull = self.solve(points[midIdx:])	# Second half                                   # T O(logn) | S O(n) - 1 array, recursive
    return self.combine(leftHull, rightHull)                                                # T(n) | S O(n) - See fn, 1 array
  
  '''Converts array of QPointF points to an array of QLineF lines'''
  def toPolygon(self, points):                                                # Fn - T O(n) | S(1)  
    polygon = []                                                              # S O(1)
    for i in range(len(points)):                                              # T O(n) - Number of points
      if i < len(points) - 1:
        polygon.append(QLineF(self.at(points, i), self.at(points, i+1)))      # T O(1) - Appending is constant | S O(n) - need extra space for each n insertion
      else:   # On last iteration connect last point to first
        polygon.append(QLineF(self.at(points, i), self.at(points, 0)))        # T O(1) - Appending is constant | S O(n) - need extra space for each n insertion
    return polygon

  '''
    NOTE
    Hulls are sorted in cw order
    The 1st element in a hull is its leftmost point
  '''

  '''Finds upper/lower tangent of each hull, then returns back indices for the left and right 2 upper/lower tangents.'''
  def findTangentIndices(self, leftHull, rightHull, findLower):                                       # Fn - T O(n) | S(1) - Technically T 2n
    # Find rightmost point of left hullleftmost and rightmost points
    leftCurrIndex = self.getRightmostPtIdx(leftHull)                                                  # T O(n) - See fn | S O(1) - 1 int
    rightCurrIdx = LEFTMOST_PT_IDX                                                                    # T O(1) | S O(1) - 1 int

    fullyOptimized = False                                                                            # T O(1) | S O(1) - 1 boolean

    while not fullyOptimized:                                                                         # T O(n) - Worst case, looping through top halves of both left (n/2) and right (n/2) hulls
      fullyOptimized = True

      # Left Side - finding optimal point
      
      leftNextIdx = leftCurrIndex - 1 # Left hull's next counter-clockwise index
      if findLower:
        leftNextIdx = leftCurrIndex + 1 # Left hull's next clockwise index

      currSlope = self.findSlope(self.at(rightHull, rightCurrIdx), self.at(leftHull, leftCurrIndex))  # T O(1) - See fn | S O(1) - 1 float
      nextSlope = self.findSlope(self.at(rightHull, rightCurrIdx), self.at(leftHull, leftNextIdx))    # T O(1) - See fn | S O(1) - 1 float

      isBetter = nextSlope < currSlope                                                                # T O(1) | S O(1) - 1 boolean
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
      
      currSlope = self.findSlope(self.at(leftHull, leftCurrIndex), self.at(rightHull, rightCurrIdx))  # T O(1) - See fn | S O(1) - 1 float
      nextSlope = self.findSlope(self.at(leftHull, leftCurrIndex), self.at(rightHull, rightNextIdx))  # T O(1) - See fn | S O(1) - 1 float

      isBetter = nextSlope > currSlope                                                                # T O(1)
      if findLower:
        isBetter = nextSlope < currSlope

      if isBetter:
        currSlope = nextSlope
        rightCurrIdx = rightNextIdx
        fullyOptimized = False
      
    return leftCurrIndex, rightCurrIdx

  '''Combines 2 hulls together (returns a list of lines)'''
  def combine(self, leftHull, rightHull):                                                             # Fn - T O(n) | O(n) - Technically T 5n, S 3n
    # Find upper tangent connecting the hulls
    leftUpperIdx, rightUpperIdx = self.findTangentIndices(leftHull, rightHull, False)                 # T O(n) - See Fn | S(1) - 2 ints 
    # Find lower tangent connecting the hulls
    leftLowerIdx, rightLowerIdx = self.findTangentIndices(leftHull, rightHull, True)                  # T O(n) - See Fn | S(1) - 2 ints 
    
    # Combine points together into new hull
    comboHull = []                                                                                                          # S(1)
    comboHull = self.addPoints(comboHull, leftHull, LEFTMOST_PT_IDX, leftUpperIdx) # Top part of left hull to keep          # T O(n), S O(n) - See Fn
    comboHull = self.addPoints(comboHull, rightHull, rightUpperIdx, rightLowerIdx) # Part of right hull to keep             # T O(n), S O(n) - See Fn
    comboHull = self.addLowerLeftPoints(comboHull, leftHull, leftLowerIdx) # Bottom part of left hull to keep               # T O(n), S O(n) - See Fn

    return comboHull

  '''Finds slope of the line made by connecting the 2 points passed in'''
  def findSlope(self, point1, point2):                                    # T O(1), S O(1)
    line = QLineF(point1, point2)                                         # S O(1) - 1 line variable
    return line.dy() / line.dx()                                          # T O(1) - Typically more expensive, but Python has optimized this

  '''Returns index of item in hull (handles logic so that hull can loop circularly).'''
  def at(self, hull, index):                                              # T O(1)
    return hull[index % len(hull)]                                        # T O(1) - Access is constant, mod is constant

  '''Adds points from an old hull to a new one'''
  def addPoints(self, newHull, oldHull, currIdx, finalIdx):               # Fn - T O(n), S O(n)
    newHull.append(self.at(oldHull, currIdx))                             # T O(1) - Appending is constant | S O(1) - just one item added to array
    while (currIdx % len(oldHull)) != (finalIdx % len(oldHull)):          # T O(n) - Size of old hull, mod is constant
        currIdx += 1
        newHull.append(self.at(oldHull, currIdx % len(oldHull)))          # T O(1) - Appending is constant, mod is constant | # S O(n) - need extra space for each n insertion

    return newHull

  '''Handles edge case for adding points to the lower left of a hull'''
  def addLowerLeftPoints(self, newHull, leftHull, leftLowerIdx):          # Fn - T O(n), S O(n)
    if len(leftHull) == 1:                                                # T O(1)
      return newHull

    while (leftLowerIdx % len(leftHull)) != LEFTMOST_PT_IDX:                            # T O(n) - Size of left hull
      newHull.append(self.at(leftHull, leftLowerIdx))                     # T O(1) - Appending is constant | S O(n) - need extra space for each n insertion
      leftLowerIdx += 1
    return newHull

  '''Returns the index of the rightmost point in hull'''
  def getRightmostPtIdx(self, hull):                        # Fn - T O(n)
    biggestXVal = max(hull, key= lambda k: k.x())           # T O(n) Worst - Depends on Python's implementation | S O(1) - int
    return hull.index(biggestXVal)                          # T O(1)