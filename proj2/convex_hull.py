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
    # Base case - combine # FIXME - FIGURE OUT HOW TO DO IT WITH 1 BASE CASE
    # if len(points) == 1:  # If just one point, have an array with 1 line pointing to itself
    #   return [QLineF(points[0], points[0])]
    if len(points) <= 2:  # If 2 points, have array with 1 line connecting the 2 points
      return points

    # Break up points
    midIdx = len(points) // 2
    leftHull = self.solve(points[:midIdx])	# First half
    rightHull = self.solve(points[midIdx:])	# Second half
    return self.combine(leftHull, rightHull)
  
  '''Converts array of QPointF points to an array of QLineF lines'''
  def toPolygon(self, points):                                            # O(n)
    # if len(points) == 1:
    #   return [QLineF(points[0], points[0])]

    # if len(points) == 2:
    #   return [QLineF(points[0], points[1])]
      
    polygon = []
    for i in range(len(points)):                                          # O(n)
      if i < len(points) - 1:
        polygon.append(QLineF(points[i], points[i+1]))
      else:   # On last iteration connect last point to first
        polygon.append(QLineF(points[i], points[0]))
    return polygon

  '''
  NOTE
  Hulls are sorted in cw order
  The 1st element in a hull is its leftmost point
  '''

  '''Finds upper tangent of each hull, then returns back indices for the 2 upper tangents.'''
  def findUpperTangent(self, leftHull, rightHull):
    # return 0, 0  # TESTING FIXME
    # Find rightmost point of left hullleftmost and rightmost points
    leftHullIdx = self.getRightmostPtIdx(leftHull)
    rightHullIdx = LEFTMOST_PT_IDX

    print('lhi', leftHullIdx)
    print('rhi', rightHullIdx)
    
    currentSlope = self.findSlope(leftHull[leftHullIdx], rightHull[rightHullIdx])
    fullyOptimized = False

    while not fullyOptimized:
      fullyOptimized = True
      
      leftHullCCWPt = leftHull[leftHullIdx - 1]   # Left hull's next counter-clockwise point
      
      print('rh', rightHull)
      print('here', rightHull[rightHullIdx])
      tempNextSlope = self.findSlope(rightHull[rightHullIdx], leftHullCCWPt)
      if tempNextSlope > currentSlope:
        currentSlope = tempNextSlope
        leftHullIdx = leftHullCCWPt
        fullyOptimized = False

      rightHullCWPt = rightHull[rightHullIdx + 1]   # Right hull's next clockwise point
      tempNextSlope = self.findSlope(leftHull[leftHullIdx], rightHullCWPt)
      if tempNextSlope < currentSlope:
        currentSlope = tempNextSlope
        rightHullIdx = rightHullCWPt
        fullyOptimized = False
      
    return leftHullIdx, rightHullIdx

  def findLowerTangent(self, leftHull, rightHull):
    return 0, 1   # TESTING

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

    print('lh', leftHull)
    print('lh1', leftHull[0])
    print('rh', rightHull)
    print('luti', leftHUpperIdx)
    print('ruti', rightHUpperIdx)
    print('llti', leftHLowerIdx)
    print('rlti', rightHLowerIdx)

    comboHull = []
    comboHull += self.grabPoints(leftHull, leftHLowerIdx, leftHUpperIdx) # Part of left hull to keep
    comboHull += self.grabPoints(rightHull, rightHUpperIdx, rightHLowerIdx) # Part of right hull to keep
    return comboHull

  '''Calculates the slope of the line connecting 2 points (formula: slope = (y2 - y1) / (x2 - x1))'''
  # def findSlope(self, point1, point2):
  #   return (point2.y() - point1.y()) / (point2.x() + point1.x())

  '''Finds slope of the line made by connecting the 2 points passed in'''
  def findSlope(self, point1, point2):
    line = QLineF(point1, point2)
    return line.dy() / line.dx()

  '''Returns index of item in hull (handles logic so that hull can loop circularly).'''
  def at(self, hull, index):
    return hull[index % len(hull)]

  def grabPoints(self, hull, firstPtIdx, lastPtIdx):
    firstPtIdx = firstPtIdx % len(hull)
    lastPtIdx = lastPtIdx % len(hull)
    return hull[firstPtIdx : lastPtIdx + 1]

  '''Returns the index of the rightmost point in hull'''
  def getRightmostPtIdx(self, hull):
    biggestXVal = max(hull, key= lambda k: k.x())
    return hull.index(biggestXVal)