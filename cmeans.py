from PIL import Image
import random
im = Image.open("lena.bmp")
def getCenters(points,numCenters): #get n centers with maximum distance between them
	centers=[points[0]]
	for i in range(numCenters-1):
		bestDist = sum((sqDistance(points[1],center))**(0.25) for center in centers)
		best = points[1]
		#best's resets to second point in image after finding furthest point.
		for point in points: #find the point farthest from intial point first, then farthest from either end,...
			dist = sum((sqDistance(point,center))**(0.25) for center in centers) #find max distance considering all centers
			if dist > bestDist: 
				bestDist = dist
				best = point
		centers.append(best)
	return centers
#associate each point in image with closest cluster
def associate(points,centers):
	zeroV = [0 for p in points[0]]
	pos = [zeroV for c in centers]
	count = [0 for c in centers]
	for point in points:
		best = 0
		bestDist = sqDistance(point,centers[0])
		for i,center in enumerate(centers):
			dist = sqDistance(point,center)
			if dist < bestDist:
				bestDist = dist
				best = i
		pos[best] = addVectors(point,pos[best])
		count[best] += 1
	return [divideVector(p,c)for p,c in zip(pos,count)]
def addVectors(v1,v2):
	return [a+b for a,b in zip(v1,v2)]
def divideVector(v,s):
	return [a/s for a in v]
#recaluclate centers for each cluster by averaging distances from each center to each point in cluster
#return the n recalculated centers.
def sqDistance(point1,point2):
	dist = 0
	for a,b in zip(point1,point2):
		dist += (a-b)**2
	return dist
p = im.getdata()
c = getCenters(p,10)
print c
for x in range(10):
	c2 = c
	c = associate(p,c)
	print c
	if c2 == c:
		break