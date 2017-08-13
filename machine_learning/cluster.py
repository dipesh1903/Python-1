
from math import sqrt
import random


class bicluster:
	def __init__(self,vec,left=None,right=None, distance=0.0,id=None):
		self.left = left
		self.right = right
		self.vec = vec
		self.id = id
		self.distance = distance


def getdata(filename):
	lines = [line for line in open(filename,'r')]
	
	colnames = lines[0].strip().split('\t')[1:]
	
	rowname=[]
	data=[]
	for line in lines[1:]:
		
		p = line.strip().split('\t')
		rowname.append(p[0])
		data.append([float(x) for x in p[1:]])
	

	return rowname,colnames,data


	def pearson(d1,d2):
	
	
	sum1 = sum(d1)
	sum2 = sum(d2)

	sumsq1 = sum([pow(i,2) for i in d1])
	sumsq2 = sum([pow(i,2) for i in d2])

	sump = sum([d1[i]*d2[i] for i in range(len(d2))])

	num = sump - (sumsq1*sumsq2)/len(d1)
	den = sqrt((sumsq1 - pow(sum1,2)/len(d1))* (sumsq2 - pow(sum2,2)/len(d1)))
	if den == 0: return 0

	return 1.0 - (num/den)

#K-MEANS CLUSTERING ALGORITHM

def kcluster(rows,distance=pearson,k=4):
	ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows]))
	for i in range(len(rows[0]))]
	
	# Create k randomly placed centroids
	clusters=[[random.random( )*(ranges[i][1]-ranges[i][0])+ranges[i][0]
	for i in range(len(rows[0]))] for j in range(k)]
	
	lastmatches=None
	for t in range(100):
		print ('Iteration %d' % t)
		bestmatches=[[] for i in range(k)]
		# Find which centroid is the closest for each row
		
		for j in range(len(rows)):
			row=rows[j]
			bestmatch=0
			for i in range(k):
				d=distance(clusters[i],row)
				if d<distance(clusters[bestmatch],row): bestmatch=i
			bestmatches[bestmatch].append(j)
		# If the results are the same as last time, this is complete
		if bestmatches==lastmatches: break
		lastmatches=bestmatches

		for i in range(k):
			avgs=[0.0]*len(rows[0])
			
			if len(bestmatches[i])>0:
				for rowid in bestmatches[i]:
					for m in range(len(rows[rowid])):
						avgs[m]+=rows[rowid][m]
				for j in range(len(avgs)):
					avgs[j]/=len(bestmatches[i])
				clusters[i]=avgs
	return bestmatches

