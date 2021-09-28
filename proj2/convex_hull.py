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
		# Sorts the points by increasing x-value - FIXME - ASK TA IF THIS IS OK, OR IF WE NEED OUR OWN QUICK SORT
		points = [item[1] for item in sorted([(pt.x(),pt) for pt in points])]
		t2 = time.time()

		

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		polygon = [QLineF(points[i],points[(i+1)%3]) for i in range(3)]
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		timeElapsed = (t2 - t1) + (t4 -t3)		# Time will be for sorting and solving combined
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(timeElapsed))	# FIXME - Ask TA - Should time elapsed include the time it takes to sort

		polygon = []

	def findUpperTangent(self, leftHull, rightHull):
		leftmost, rightmost = leftHull[0], rightHull[-1]	# Find leftmost and rightmost points

		temp = line(p,q)
		done = 0
		while not done:
			done = 1
			while temp != is not upper tangent to L:
				r = p's counterclockwise neighbor
				temp = line(r,q)
				p = r
				done = 0
			while temp is not upper tangent to R:
				r = q's clockwise neighbor
				temp = line(p,r)
				q = r
				done = 0
		return temp

		# def findLowerTangent(self, leftHull, rightHull):
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


	'''Sorts points in hull in clockwise order (array can be traversed backwards for counter-clockwise).'''
	def sortHull(self):
		pass

	'''Returns index of item in hull (handles logic so that hull can loop circularly).'''
	def at(self, hull, index):
		return hull[index % len(hull)]

	'''Finds the next clockwise neighbor in a hull.'''
	def findCW(self, hull, currIndex):
		return hull[currIndex + 1]

	'''Finds the next counter-clockwise neighbor in a hull.'''
	def findCCW(self, hull, currIndex):
		return hull[currIndex - 1]