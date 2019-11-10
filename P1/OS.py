#10527142
import threading
import time
import queue
import multiprocessing
from multiprocessing import Queue
import multiprocessing as mp

def workone(worklist):
	n = len(worklist)
	for i in range(n-1):
		for j in range(0, n-i-1):
			count = 0
			if worklist[j] > worklist[j+1] :
				worklist[j], worklist[j+1] = worklist[j+1], worklist[j]
				count +=1
		if count==0:
			break
	
	return worklist
	
def worktwo(worklist, knum):
	threadsBS = []
	tempA = [worklist[i:i+knum] for i in range(0,len(worklist),knum)] #分成K分
	#分給K個thread做冒泡排序
	for i in range(len(tempA)):
		threadsBS.append(threading.Thread(target = workone, args = (tempA[i],)))
		threadsBS[i].start()
	#等所有人都結束
	for i in range(len(tempA)) :
		threadsBS[i].join()
	
	#K-1個thread做合併排序
	numk = knum -1
	q = queue.Queue() 	#回傳THREAD的值要用QUEUE來接(THREAD不會回傳值)  這是新創一個放QUEUE的地方
	threadsMS = []
	margetemp = [] 			#放暫時的陣列
	margetemp = margeQ(margetemp, tempA[0],q)
	for i in range(len(tempA)):
		threadsMS.append(threading.Thread(target = margeQ, args = (q.get(),tempA[i],q,)))
		threadsMS[i].start()
	#for i in range(len(tempA)):
		threadsMS[i].join()
	
	#print(q.get())
	worklist = q.get()
	
	return worklist	
	
def workfour(worklist, knum):	
	#分割成K分
	#各自做冒泡(呼叫任務1)
	tempA = [worklist[i:i+knum] for i in range(0,len(worklist),knum)]
	for i in range(len(tempA)) :
		workone(tempA[i])
		
	#全部MERGE到ANS裡面
	#n = len(worklist)
	#如果有K個ARRAY  那就做K-1次
	long = len(tempA)
	margetemp = [] 			#放暫時的陣列
	margetemp = marge(margetemp, tempA[0])
	for i in range(1, long): 
		margetemp = marge(margetemp, tempA[i] )

	return margetemp
	
def marge(margetemp, tempA): #給兩list 幫你合在一起排序
	#print("in marge def", end="")
	#print(margetemp, tempA)
	temp = []
	while margetemp and tempA :
		if margetemp[0] <= tempA[0]:
			temp.append(margetemp.pop(0))
		else :
			temp.append(tempA.pop(0))
	#出來代表有人空	

	if margetemp and not tempA : #temp 空
		while (len(margetemp) > 0) :
			temp.append(margetemp.pop(0))
	elif tempA and not margetemp : #marge 空
		while (len(tempA) > 0) :
			temp.append(tempA.pop(0))
	return temp
	
def margeQ(margetemp, tempA, q): #給兩list 幫你合在一起排序 **給THREAD專用的 Q是QUEUE
	#print("in marge def", end="")
	#print(margetemp, tempA)
	temp = []
	while margetemp and tempA :
		if margetemp[0] <= tempA[0]:
			temp.append(margetemp.pop(0))
		else :
			temp.append(tempA.pop(0))
	#出來代表有人空	

	if margetemp and not tempA : #temp 空
		while (len(margetemp) > 0) :
			temp.append(margetemp.pop(0))
	elif tempA and not margetemp : #marge 空
		while (len(tempA) > 0) :
			temp.append(tempA.pop(0))
	#return temp 不用RETURN
	q.put(temp)
	
def margeP(margetemp, tempA, new): #給兩list 幫你合在一起排序 
	#print("in marge def", end="")
	#print(margetemp, tempA)
	temp = []
	while margetemp and tempA :
		if margetemp[0] <= tempA[0]:
			temp.append(margetemp.pop(0))
		else :
			temp.append(tempA.pop(0))
	#出來代表有人空	

	if margetemp and not tempA : #temp 空
		while (len(margetemp) > 0) :
			temp.append(margetemp.pop(0))
	elif tempA and not margetemp : #marge 空
		while (len(tempA) > 0) :
			temp.append(tempA.pop(0))
	#return temp 不用RETURN
	return temp
	
def workonePBS(worklist, q): #Process Bubble Sort
	n = len(worklist)
	for i in range(n-1):
		for j in range(n-i-1):
			if worklist[j] > worklist[j+1] :
				worklist[j], worklist[j+1] = worklist[j+1], worklist[j]
	
	q.put(worklist)

def writeoutput(worklist, runningtime, filename):
	filenamewrite = filename + "_output.txt" 
	filewrite = open(filenamewrite,'w')
	for index in range(len(worklist)):
		filewrite.write(str(worklist[index]))
		filewrite.write(" ")
	filewrite.write("\n")
	filewrite.write("執行時間:")
	filewrite.write(str(runningtime))
	filewrite.close()

if __name__=='__main__' :
	filename = input("輸入input檔名(單獨一個0結束):" )
	while filename != '0' : 
		filenamereade = filename + '.txt' #完整檔名
		file = open(filenamereade,'r') #開黨
		worklist = [] #工作地方
		theNum = 0 				 #讀取要做的哪一個小題
		theNum = file.readline() #讀取要做的哪一個小題
		missionnum = int(theNum)
		print("missionnum:", end = "" )
		print(missionnum) 			 #決定要做的小題
		
		allinput = file.read() #讀全部的資料
		worklist = allinput.split() #資料處理
		worklist = list(map(int, worklist)) #str轉int
		if missionnum == 1:
			star = time.clock() #開始時間
			workone(worklist)
			end = time.clock() #結束時間
		elif missionnum == 2 :
			knum = input("輸入k(k>0的整數):" )
			knum = int(knum)
			if knum < 1 : break 
			star = time.clock() #開始時間
			worklist = worktwo(worklist, knum)
			end = time.clock() #結束時間
		elif missionnum == 3 :
			knum = input("輸入k(k>0的整數):" )
			knum = int(knum)
			if knum < 1 : break 
			star = time.clock() #開始時間
			#worklist = workthree(worklist, knum)
			processBS = []
			knum = len(worklist)//knum
			insideTowSort = []
			tempA = [worklist[i:i+knum] for i in range(0,len(worklist),knum)] #分成K分
			#分給K個Process做冒泡排序
			#q = Queue()
			#創造多個PROCESS
			pool = multiprocessing.Pool(processes=4) #創造池
			for i in range(len(tempA)):
				#processBS.append(multiprocessing.Process(target = workonePBS, args = (tempA[i],q,)))
				processBS=pool.apply_async(workone,(tempA[i],))
				insideTowSort.append(processBS.get())

			pool.close() # 關閉pool, 則不會有新的程序新增進去
			pool.join() 

			#for i in range(len(tempA)):
				#insideTowSort.append(processBS.get())
			#print("insideTowSort:", end="") #測試
			#print(insideTowSort) #測試
			#用k-1個PROCESS做MERGE
			
			numk = knum-1
			poolforMer = multiprocessing.Pool(processes=4) #創造池
			#qP = Queue()
			#processMS = []
			#margetemp = []
			ans = []
			#insideTowSort.append(ans)
			i = 0 
			while i < len(insideTowSort):
				if i != len(insideTowSort)-1 :
					processMS=poolforMer.apply_async(margeP,(insideTowSort[i],insideTowSort[i+1],insideTowSort))
					#processMS=multiprocessing.Process(target=margeP,args=(insideTowSort[i],insideTowSort[i+1],insideTowSort))
					ans.append(processMS.get())
					insideTowSort.append(ans[len(ans)-1])
				i+=2

			poolforMer.close() # 關閉pool, 則不會有新的程序新增進去
			poolforMer.join() 
			
			#for i in range(len(insideTowSort)):
			worklist = insideTowSort[len(insideTowSort)-1]
			
			end = time.clock() #結束時間
		elif missionnum == 4 :
			knum = input("輸入k(k>0的整數):" )
			knum = int(knum)
			if knum < 1 : break 
			star = time.clock() #開始時間
			worklist = workfour(worklist, knum)
			end = time.clock() #結束時間
		else :
			print("It's not right num of mission.") #如果是錯的小題就跳出
			missionnum = 0
			temp = ""
			file.close() #這裡也不要忘記初始化
			break 

		writeoutput(worklist, end - star, filename) #寫檔案出來
		file.close() #關掉檔案
		#print (end - star) #印時間
		#time.clock()是CPU的執行時間
		#time.time()程式的執行時間
		#下面都是初始化
		missionnum = 0
		temp = ""
		filename = input("輸入input檔名(單獨一個0結束):" )