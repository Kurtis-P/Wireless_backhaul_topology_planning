from math import sqrt,radians
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import time
import numpy
import os

start_time=time.time()
start_time_s=time.localtime(start_time);
print('开始时间：'+time.asctime(start_time_s))
BASEDIR = os.path.dirname(__file__)
time_struct=time.localtime()
time_str=[]
for i in range(6):
	time_str.append(str(time_struct[i]))
time_name='_'.join(time_str)
BASEDIR=os.path.join(BASEDIR,time_name)
FIG=os.path.join(BASEDIR,'FIG')
os.makedirs(FIG)
DATA=os.path.join(BASEDIR,'DATA')
os.makedirs(DATA)
# cluster points
points=[]
#f1=open('x.txt','r')
f1=open('x.txt','r')
x=f1.readlines()
# f2=open('latitude.txt','r')
f2=open('y.txt','r')
y=f2.readlines()
points=[[float(x[i].strip()),float(y[i].strip())] for i in range(len(x))]
f1.close()
f2.close()
# 计算两点距离
# x为经度，y为纬度
def distance_2point(x1, y1, x2, y2):
	return sqrt((x2-x1)**2 + (y2-y1)**2)
	#[x1,x2,y1,y2]=map(radians,[x1,x2,y1,y2])
	#return 6378*math.acos(math.cos(y2)*math.cos(y1)*math.cos(x1-x2)+math.sin(y1)*math.sin(y2))


# 计算平均距离
def volume_estimation(cluster, center):
	num_of_points = len(cluster)
	distance = []
	for i in range(num_of_points):
		distance.append(distance_2point(center[0], center[1], cluster[i][0], cluster[i][1]))

	return sum(distance)/num_of_points


# 定义新的簇中心
def new_cluster_centers(cluster):
	x=0
	y=0
	for i in cluster:
		x+=i[0]
		y+=i[1]
	length = len(cluster)
	return (x/length, y/length)


# 各中心的距离
def center_distance(centers):
	D_ij = {}
	# offset coeficient
	k = 0
	for i in range(len(centers)):
		for j in range(k, len(centers)):
			if i == j:
				pass
			else:
				D_ij[(i,j)] = distance_2point(centers[i][0], centers[i][1], centers[j][0], centers[j][1])
		k +=1
	return D_ij


# MSE
def standart_deviation(values, center):
	n = len(values) 
	x_coord = []
	y_coord = []
	for i in range(n):
		x_coord.append((values[i][0]-center[0])**2)
		y_coord.append((values[i][1]-center[1])**2)

	x = sqrt(sum(x_coord)/n)
	y = sqrt(sum(y_coord)/n)

	return (x,y)

#重新归类
def cluster_points_distribution(centers, points):
	centers_len = len(centers)
	points_len = len(points)
	distances = []
	distance = []

	# define array for clusters
	clusters = [[] for i in range(centers_len)]

	# iteration throught all points
	for i in range(points_len):
		# iteration throught all centers
		for j in range(centers_len):
			distance.append(distance_2point(centers[j][0], centers[j][1], points[i][0], points[i][1]))
		distances.append(distance)
		distance = []

	# distribution
	for i in range(points_len):
		ind = distances[i].index(min(distances[i]))
		clusters[ind].append(points[i])

	return clusters


def cluster_division(cluster, center, dev_vector):
	#divide only center of clusters

	# coeficient
	k = 0.5

	max_deviation = max(dev_vector)
	index = dev_vector.index(max(dev_vector))
	g = k*max_deviation

	# defining new centers
	center1 = list(center)
	center2 = list(center)
	center1[index] += g
	center2[index] -= g

	cluster1 = []
	cluster2 = []

	return tuple(center1), tuple(center2)


def cluster_union(cluster1, cluster2, center1, center2):
	x1 = center1[0]
	x2 = center2[0]
	y1 = center1[1]
	y2 = center2[1]
	n1 = len(cluster1)
	n2 = len(cluster2)

	x = (n1*x1 + n2*x2)/(n1+n2)
	y = (n1*y1 + n2*y2)/(n1+n2)
	center = (x,y)
	cluster = cluster1 + cluster2

	return center, cluster

def test(clusters,centers):
	for i in clusters:
		if len(i)<1:
			num=clusters.index(i)
			clusters.remove(i)
			centers.remove(centers[num])
	return

def clusterize():

	# initial values
	K = 20 # max cluster number
	THETA_N = 7 # for cluster elimination
	THETA_S = 8 # for cluster division
	THETA_C = 3 # for cluster union
	L = 3 # 
	I = 30 # max number of iterations
	N_c = 10 # number of primary cluster centers

	distance = [] # distances array
	centers = [] # clusters centers
	clusters = [] # array for clusters points
	iteration = 1 # number of current iteration
	
	centers.append(points[0]) # first cluster center

	while iteration <= I:
		
		if(iteration==1):
			time_old=start_time
		else:
			time_old=time_now
		#重新分簇
		if len(centers) <= 1:
			clusters.append(points)
		else:
			clusters = cluster_points_distribution(centers, points)
		
		flag=True
		# 去掉样本数过小的簇（与距离最近的簇融合）
		for i in range(len(clusters)):
			if len(clusters[i]) <= THETA_N:
				flag=False
				print('样本过小！\n')
				D_ij=center_distance(centers)
				dis=[]
				for j in range(len(clusters)):
					dis.append(D_ij[(i,j)])
				key=dis.index(min(D_ij))
				clusters[key].append(item for item in clusters[i])
				del clusters[i]
				break
			else:
				pass
			break
			if not flag:
				flag=True
				if len(centers) <= 1:
					clusters.append(points)
				else:
					clusters = cluster_points_distribution(centers, points)
		
		test(clusters,centers)
		# 寻找新的聚类中心
		centers = []
		for i in range(len(clusters)):
			centers.append(new_cluster_centers(clusters[i]))

		# 计算每个类的类内平均距离
		D_vol = []
		for i in range(len(centers)):
			D_vol.append(volume_estimation(clusters[i], centers[i]))

		# 计算所有类的总体平均距离
		if len(clusters) <= 1:
			D = 0
		else:		
			cluster_length = []
			vol_sum = []
			for i in range(len(centers)):
				cluster_length.append(len(clusters[i]))
				vol_sum.append(cluster_length[i]*D_vol[i])

			D = sum(vol_sum)/len(points)


		# 判断停止、分裂或合并
		if iteration >= I:
			THETA_C = 0#算法结束

		# elif (N_c >= 2*K) or (iteration % 2 == 0):
			# pass#跳过分裂处理

		elif (K/2<K<2*K) and (iteration%2==1):
			#进行分裂处理
			vectors = []
			for i in range(len(centers)):
				vectors.append(standart_deviation(clusters[i], centers[i]))

			max_s = []
			for v in vectors:
				max_s.append(max(v[0], v[1]))

			for i in range(len(max_s)):
				length = len(clusters[i])
				coef = 2*(THETA_N+1)

				if (max_s[i] > THETA_S) and ((D_vol[i]>D and length>coef) or N_c<float(K)/2):
					center1, center2 = cluster_division(clusters[i], centers[i], vectors[i])
					del centers[i]
					centers.append(center1)
					centers.append(center2)
					N_c += 1

				else:
					pass
		
		elif (K/2<K<2*K) and (iteration%2==0):	
			#进行合并处理
			D_ij = center_distance(centers)
			rang = {}
			for coord in D_ij:
				if D_ij[coord] < THETA_C:
					rang[coord] = (D_ij[coord])
				else:
					pass

			for key in rang.keys():
				cluster_union(clusters[key], clusters[key.next()], centers[key], centers[key.next()])
				N_c -= 1

		plotfig(clusters,centers,iteration)
		time_now=time.time()
		print('迭代'+str(iteration)+'用时：'+str(time_now-time_old)+'s')
		iteration += 1
		
	return clusters,centers,max_s

def plotfig(clusters,centers,I):
	color=['peru','dodgerblue','brown','gold','dimgrey','midnightblue','lavender','navy','violet','thistle','chartreuse','olive',
			'orange','springgreen','burlywood','fuchsia','darkslategrey','orangered','tomato','red','khaki','darkgoldenrod','deeppink','skyblue',
			'darkgray','darkblue','deepskyblue','wheat',
			'peru','dodgerblue','brown','gold','dimgrey','midnightblue','lavender','navy','violet','thistle','chartreuse','olive',
			'orange','springgreen','burlywood','fuchsia','darkslategrey','orangered','tomato','red','khaki','darkgoldenrod','deeppink','skyblue',
			'darkgray','darkblue','deepskyblue','wheat']
	key=0
	for i in clusters:
		for j in i:
			plt.plot(j[0],j[1],'.',color=color[key%29])
		key+=1
	key=0
	for i in centers:
		plt.plot(i[0],i[1],'*',color='black')
		plt.annotate(s=(str(key+1)),xy=i)
		key+=1
	name='iteration_'+str(I)+'.png'
	path=os.path.join(FIG,name)
	plt.savefig(path)
	plt.clf()
	plt.close('all') 
	
if __name__ == '__main__':
	cl,cen,max_s= clusterize()
	# color=['r','b','g','gold','dimgrey','midnightblue','lavender','navy','violet','thistle','chartreuse','olive','r','b','g','gold','dimgrey','midnightblue','lavender','navy','violet','thistle','chartreuse','olive','r','b','g','gold','dimgrey','midnightblue','lavender','navy','violet','thistle','chartreuse','olive']
	# key=0
	# print(len(cl))
	# print(len(cen))
	# print(len(max_s))
	# for i in cl:
		# for j in i:
			# plt.plot(j[0],j[1],'.',color=color[key])
		#plt.show()
		# key+=1
	# key=0
	# for i in cen:
		# plt.plot(i[0],i[1],'*',color='black')
		# plt.annotate(s=(str(key)),xy=i)
		# key+=1
		# print(key)
	# plt.show()
	#print(max_s)
	test(cl,cen)
	for i in range(len(cl)):
		name=str(i)+'_'+str(len(cl[i]))+'.txt'
		filepath=os.path.join(DATA,name)
		f=open(filepath,'w')
		for j in cl[i]:
			f.write(str(j[0])+' '+str(j[1])+'\n')
		f.close()
	end_time=time.time()
	end_time_s=time.localtime(end_time)
	print('结束时间：'+time.asctime(end_time_s))
	time=end_time-start_time;
	print('进程用时：'+str(time)+'s')
	




