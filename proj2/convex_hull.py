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

    t1 = time.time()
    # Sorts the points by increasing x-value
    points.sort(key= lambda k: k.x())	# Overwrites points with same but new order
    t2 = time.time()

    t3 = time.time()
    polygon = self.solve(points)
    t4 = time.time()

    self.showTangent(polygon, BLUE);

    # when passing ines to the display, pass a list of QLineF objects.  Each QLineF
    # object can be created with two QPointF objects corresponding to the endpoints
    self.showHull(polygon,RED)
    timeElapsed = (t2 - t1) + (t4 -t3)		# Time will be for sorting and solving combined
    self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(timeElapsed))	# FIXME - Ask TA - Should time elapsed include the time it takes to sort

    polygon = []

  '''Divide-and-conquer Convex Hull Solver'''
  def solve(self, points):
    # Base case - combine # FIXME - FIGURE OUT HOW TO DO IT WITH 1 BASE CASE
    if len(points) == 2:
    	return QLineF(points[0], points[1])	# Might have to convert to list?
    # Break up points into they are size 1
    midIdx = len(points) // 2
    leftHull = self.solve(points[:midIdx])	# First half
    rightHull = self.solve(points[midIdx:])	# Second half
    return self.combine(leftHull, rightHull)	

  '''Finds upper tangent of each hull, then returns back indices for the 2 upper tangents.'''
  def findUpperTangent(self, leftHull, rightHull):
    # Find rightmost point of left hullleftmost and rightmost points
    leftHullIdx = leftHull.getRightmostPtIdx()
    rightHullIdx = rightHull.getLeftmostPtIdx() # Hulls start with leftmost point
    
    temp = QLineF(leftHull[leftHullIdx], rightHull[rightHullIdx])
    bestSlope = self.findSlope(temp)
    done = False

    while not done:
      done = True
      
      # while temp != is not upper tangent to L:
      # while self.findSlope(temp) < bestSlope:   # FIXME - Does this work???
      while True: # FIXME FIXME FIXME
        leftHullCCWPt = leftHull[leftHullIdx - 1] # Rotate to next point in left hull counter-clockwise
        temp = QLineF(leftHullCCWPt, rightHullIdx)
        leftHullIdx = leftHullCCWPt
        done = False

      # while temp != is not upper tangent to R:
      while True: # FIXME FIXME FIXME
        rightHullCWPt = rightHull[rightHullIdx + 1] # Rotate to next point in right hull clockwise
        temp = QLineF(leftHullIdx, rightHullCWPt)
        rightHullIdx = rightHullCWPt
        done = False
    
    return temp # Type: QLineF

  def findLowerTangent(self, leftHull, rightHull):
    pass
    # leftmost, rightmost = leftHull[0], rightHull[-1]	# Find leftmost and rightmost points

    # temp = line(p,q)
    # done = 0
    # while not done:
    # 	done = 1
    # 	while temp != is not lower tangent to L:
    # 		r = p's clockwise neighbor
    # 		temp = line(r,q)
    # 		p = r
    # 		done = 0
    # 	while temp is not lower tangent to R:
    # 		r = q's counter-clockwise neighbor
    # 		temp = line(p,r)
    # 		q = r
    # 		done = 0
    # return temp

  '''Combines 2 hulls together (returns a list of lines)'''
  def combine(self, leftHull, rightHull):
    # Find upper tangent connecting the hulls
    leftHUpperIdx, rightHUpperIdx = self.findUpperTangent(leftHull, rightHull)
    # Find lower tangent connecting the hulls
    leftHLowerIdx, rightHLowerIdx = self.findLowerTangent(leftHull, rightHull)
    # Connect the hulls with the 2 tangent lines
    comboHull = Hull()
    comboHull.append(leftHull[leftHLowerIdx:leftHUpperIdx])   # Part of left hull to keep
    comboHull.append(QLineF(leftHull[leftHUpperIdx], rightHull[rightHUpperIdx]))    # Upper tangent connection
    comboHull.append(rightHull[rightHUpperIdx:rightHLowerIdx])    # Part of right hull to keep
    comboHull.append(QLineF(rightHull[rightHLowerIdx], leftHull[leftHLowerIdx]))    # Lower tangent connection

    # return QLineF(leftHull[0],rightHull[0])
    return comboHull

  '''Calculates the slope of the line connecting 2 points (formula: slope = (y2 - y1) / (x2 - x1))'''
  # def findSlope(self, point1, point2):
  #   return (point2.y() - point1.y()) / (point2.x() + point1.x())

  def findSlope(self, line):
    point1 = line[0]
    point2 = line[1]
    return (point2.y() - point1.y()) / (point2.x() + point1.x())


class Hull:   
  hull = []   # List of QLineFs

  # Hulls are sorted in cw order
  # The 1st element in a hull is its leftmost point

  def __init__(self, line):
    self.hull = [line]

  '''Overloading the [] operator - returns index of item in hull (handles logic so that hull can loop circularly).'''
  def __getitem__(self, index):
      return self.hull[index % len(self.hull)]

  '''Returns the index of the leftmost point in hull'''
  def getLeftmostPtIdx(self):
    return 0

  '''Returns the index of the rightmost point in hull'''
  def getRightmostPtIdx(self):
    biggestXVal = max(self.hull, key= lambda k: k.x())
    return self.hull.index(biggestXVal)

  '''Finds the next clockwise neighbor in a hull.'''
  def findCW(self, hull, currIndex):
    return hull[currIndex + 1]

  '''Finds the next counter-clockwise neighbor in a hull.'''
  def findCCW(self, hull, currIndex):
    return hull[currIndex - 1]

  # '''Returns index of item in hull (handles logic so that hull can loop circularly).'''
  # def at(self, hull, index):
  #   return hull[index % len(hull)]