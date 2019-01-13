#Dijkstra

import math

def cal_distance(a,b):
	return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def remo(list,obj):
	try:
		list.remove(obj)
	except:
		pass
	
def judge(OnOffSet,D_ij,num,style):
	flag=True
	#找起点
	start=[]
	full=[]
	for i in range(len(OnOffSet)):
		if(i<num)and(sum(OnOffSet[i])<4*style[i]):
			start.append(i)
		elif(i<num)and(sum(OnOffSet[i])>=4*style[i]):
			full.append(i)
		elif(i>=num)and(sum(OnOffSet[i])==1):
			start.append(i)
	for i in range(len(OnOffSet)):
		n=sum(OnOffSet[i])
		if(n==0):
			flag=False
	#print(start)
	
	for i in range(num):
		xuhao=[]
		num_p=sum(OnOffSet[i])
		for j in range(len(OnOffSet[i])):
			if OnOffSet[i][j]==1:
				tiao=1
				num_p+=1
				xuhao.append(j)
				if(sum(OnOffSet[j])==2):
					tiao=2
					num_p+=1
					for k in range(len(OnOffSet[j])):
						if (OnOffSet[j][k]==1)and(k!=i):
							son2=k
					xuhao.append(son2)
					if(sum(OnOffSet[son2])==1):
						num_p+=1
						remo(start,j)
						remo(start,son2)
						remo(start,OnOffSet[son2].index(1))
						full.append(j)
						full.append(son2)
						full.append(OnOffSet[son2].index(1))
		#print(style,num)
		#print(num_p)
		if(num_p/2>6*style[i]):
			full.append(i)
			remo(start,i)
			for k in xuhao:
				remo(start,k)
				full.append(k)
	#print(start)
	#print(full)
	#print(D_ij)
	for ii in range(len(D_ij)):
		for jj in range(len(D_ij)):
			#print(ii,jj)
			if (ii in start) and (not(jj in start))and(not(jj in full)):
				#print('T')
				pass
			else:
				D_ij[ii][jj]=1e10
	return D_ij,flag

def find_min(list):
	len_a=len(list)
	len_b=len(list)
	mini=[]
	label=[]
	for i in range(len_a):
		mini.append(min(list[i]))
		label.append(list[i].index(min(list[i])))
	a=mini.index(min(mini))
	b=label[a]
	return a,b

def print_list(list):
	len_a=len(list)
	len_b=len(list)
	f=open('OnOffSet.txt','w')
	for i in range(len_a):
		for j in range(len_b):
			print(str(list[i][j])+' ')
			f.write(str(list[i][j])+' ')
		print('\n')
		f.write('\n')
	f.close()
	return

def Dijkstra(centers,points,style):
	#style表示基站的类型，1为ruralstar，2为蝴蝶型
	points=centers+points
	#print(points)
	num=len(centers)
	#print(num)
	num_points=len(points)-num
	suppot=sum([6*style[i] for i in range(len(style))])
	if(num_points>=suppot):
		print("ERROR3!")
		return
	D_ij=[]
	OnOffSet=[]
	for i in range(len(points)):
		D_ij.append([])
		OnOffSet.append([])
		for j in range(len(points)):
			D_ij[i].append(1e10)
			OnOffSet[i].append(0)
	# inn=[1e10 for i in range(len(points))]
	# D_ij=[inn for i in range(len(points))]
	# innn=[0 for i in range(len(points))]
	# OnOffSet=[innn for i in range(len(points))]#0断1通
	for k in range(len(points)):
		for n in range(len(points)):
			if(k!=n):
				dis=cal_distance(points[k],points[n])
				D_ij[k][n]=math.log(dis,10)
			elif(k==n):
				D_ij[k][n]=1e10
			OnOffSet[k][n]=0
	while(True):
		D_ij_1=[]
		for k in range(len(points)):
			for n in range(len(points)):
				if(k!=n):
					dis=cal_distance(points[k],points[n])
					D_ij[k][n]=math.log(dis,10)
				elif(k==n):
					D_ij[k][n]=1e10
		D_ij_1,flag=judge(OnOffSet,D_ij,num,style)
		if flag:
			break;
		#print(D_ij_1)
		a,b=find_min(D_ij_1)
		#print(D_ij[a][b])
		if(D_ij_1[a][b]>10)and(a,b>num-1):
			print("ERROR1!")
			print(D_ij_1[a][b])
			print(OnOffSet)
			return
		elif(D_ij_1[a][b]>20):
			print("ERROR2!")
			return
		OnOffSet[a][b]=1
		OnOffSet[b][a]=1
		#print(OnOffSet)
	for i in range(len(points)):
		for j in range(len(points)):
			if(i<num)and(j<num)and(i!=j)and(D_ij[i][j]<=50):
				OnOffSet[i][j]=2
	print_list(OnOffSet)
	return OnOffSet
	
if __name__=="__main__":
	f=open('0_10.txt')
	d=f.readlines()
	data=[]
	for item in d:
		item=str(item).strip().split(' ')
		lis=[float(j) for j in item]
		data.append(lis)
	centers=[data[0]]
	#print(centers)
	points=data[1:]
	#print(points)
	style=[2]
	Dijkstra(centers,points,style)
