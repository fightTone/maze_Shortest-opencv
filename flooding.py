import cv2
import numpy as np
import threading
import colorsys
import pprint

class Point(object):
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

rw = 2
p = 0
start = Point()
end = Point()

dir4 = [Point(-1,-1),Point(1,1),Point(0,-1),Point(0,1),Point(1,0),Point(-1,0)]

def BFS(s,e):
	global img, h, w
	const = 2000

	found = False
	q = []
	v = [[0 for j in range(w)] for i in range(h)]
	parent = [[Point() for j in range(w)] for i in range(h)]

	q.append(s)
	v[s.y][s.x] = 1
	while len(q) > 0:
		p = q.pop(0)

		for d in dir4:
			cell = p + d
			if (cell.x >=0 and cell.x < w and cell.y >=0 and cell.y < h and v[cell.y][cell.x] == 0 and (img [cell.y][cell.x][0] != 0 or img [cell.y][cell.x][1] != 0 or img [cell.y][cell.x][2] != 0)):
				q.append(cell)
				v[cell.y][cell.x] = v[p.y][p.x] + 1

				img[cell.y][cell.x] =list(reversed([ i*255 for i in colorsys.hsv_to_rgb(v[cell.y][cell.x]/const,12,271)]))

				parent[cell.y][cell.x] = p

				if cell == e:
					found = True
					del q[:]
					break
	path = []
	store = []
	if found :
		p = e
		while p != s:
			path.append(p)
			p = parent[p.y][p.x]
		path.append(p)
		path.reverse()
		
		"The coordinates: \n"
		for p in path:
			cv2.rectangle(img, (p.x-2, p.y-2), (p.x+2, p.y+2), (225,255,0), 1 )
			# print "("+str(p.x)+", "+str(p.y)+")"
			cord = (p.x,p.y)
			store.append(cord)
			img[p.y][p.x] = [255,255,0]
		
		# pprint.pprint(store)
		i=1
		endz = len(store)
		print endz
		final =[]
		for x in store:
			
			if i == endz:
				break
			# print str(x[0]) + "==" + str(store[i][0])
			elif x[0] < store[i][0] and x[1] == store[i][1]:
				# print "0 degree"
				dis = [(x[0],x[1]),0]
				final.append(dis)
			elif x[0] > store[i][0] and x[1] == store[i][1]:
				# print "180 degree"
				dis = [(x[0],x[1]),180]
				final.append(dis)
			elif x[0] == store[i][0] and x[1] < store[i][1]:
				# print "270 degree"
				dis = [(x[0],x[1]),270]
				final.append(dis)
			elif x[0] == store[i][0] and x[1] > store[i][1]:
				# print "90 degree"
				dis = [(x[0],x[1]),90]
				final.append(dis)
			elif x[0] < store[i][0] and x[1] < store[i][1]:
				# print "315 degree"
				dis = [(x[0],x[1]),315]
				final.append(dis)
			elif x[0] > store[i][0] and x[1] > store[i][1]:
				# print "135 degree"
				dis = [(x[0],x[1]),135]
				final.append(dis)
			elif x[0] > store[i][0] and x[1] < store[i][1]:
				# print "225 degree"
				dis = [(x[0],x[1]),225]
				final.append(dis)
			elif x[0] < store[i][0] and x[1] > store[i][1]:
				# print "45 degree"
				dis = [(x[0],x[1]),45]
				final.append(dis)
			
			else:
				print " somethings wrong"
			i+=1
			# elif x[0] < store[i][0] and x[1] < store[i][1]:
			# 	print "0 degree"

		pprint.pprint(final)
		print "Path Found"

	else:
		print "Path Not Found"
		



def mouse_event(event,pX,pY,flags,param):

	global img, start, end, p

	if event == cv2.EVENT_LBUTTONUP:
		if p==0:
			cv2.rectangle(img, (pX-rw, pY-rw), (pX+rw, pY+rw), (0,0,255), -1 )
			start = Point(pX, pY)
			print("start = ", start.x, start.y)
			p+=1
		elif p==1:
			cv2.rectangle(img, (pX-rw, pY-rw), (pX+rw, pY+rw), (0,200,50), -1 )
			end = Point(pX, pY)
			print("end = ", end.x, end.y)
			p+=1

def disp():
	global img
	cv2.imshow("Image", img)
	cv2.setMouseCallback('Image', mouse_event)
	while True:
		cv2.imshow("Image", img)
		cv2.waitKey(1) 
#original
# img = cv2.imread("mazeit.jpg", cv2.IMREAD_GRAYSCALE)
# _, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)

#for phil_maze.png
img = cv2.imread('mazeit.jpg',cv2.IMREAD_GRAYSCALE)
_, img = cv2.threshold(img, 12,255, cv2.THRESH_BINARY)

img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
h, w = img.shape[:2]

print ("Select start and end points : ")

t = threading.Thread(target=disp, args=())
t.daemon = True
t.start()

while p < 2:
	pass

BFS(start,end);
disp()

