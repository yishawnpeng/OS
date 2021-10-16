#10527142
import os
import copy

class Process :
	def __init__(self, ID, CPUburst, ArrivalTime, Priority):	#每個人自己的資料	CPUB1-6是為了算TURNAROUND時候因為B被減少了
		self.ID = int(ID)
		self.CPUburst = int(CPUburst)
		self.CPUburst2 = int(CPUburst)
		self.CPUburst3 = int(CPUburst)
		self.CPUburst4 = int(CPUburst)
		self.CPUburst5 = int(CPUburst)
		self.CPUburst6 = int(CPUburst)
		self.ArrivalTime = int(ArrivalTime)
		self.Priority = int(Priority)
		
	def waitT(self, whatTime, mode) :				#每個人自己的WAITTIME 和 不同任務分別
		if mode == 1 :
			self.waittimeFCFS = int(whatTime)
		elif mode == 2 :
			self.waittimeRR = int(whatTime)
		elif mode == 3 :
			self.waittimePSJF = int(whatTime)
		elif mode == 4 :
			self.waittimeNPSJF = int(whatTime)
		elif mode == 5 :
			self.waittimePRIORITY = int(whatTime)	
			
	def turnaroundT(self, loneTime, mode) :			#每個人自己的TURNAROUNDTIME 和 不同任務分別
		if mode == 1 :
			self.turnaroundtimeFCFS = int(loneTime)
		elif mode == 2 :
			self.turnaroundtimeRR = int(loneTime)
		elif mode == 3 :
			self.turnaroundtimePSJF = int(loneTime)
		elif mode == 4 :
			self.turnaroundtimeNPSJF = int(loneTime)
		elif mode == 5 :
			self.turnaroundtimePRIORITY = int(loneTime)	
			
	def isuseornot(self, TF) :				#第三個任務的設定 1有0沒有
		self.isuse = int(TF)
		
	def ischeckornot(self, TTFF) :			#第五個任務設定
		self.ischeck = TTFF
		
	def rCheck():
		return self.ischeck
		
	def ruse():
		return self.isuse
		
def sortforID( mission ) :			#回傳一個用ID排的List
	ans = mission.copy()
	for i in range(0, len(ans)-1) :
		for j in range(0, len(ans)-1) :
			if ans[j].ID > ans[j+1].ID :	
				ans[j], ans[j+1] = ans[j+1], ans[j]
				
	return ans

def FCFSarrival( cleanlist ) :		#給一個list回傳依照抵達時間排列好的list (+ID)
	n = len(cleanlist)
	ans = cleanlist.copy()
	for i in range(0, n-1) :
		for j in range(0, n-i-1) :
			if ans[j].ArrivalTime > ans[j+1].ArrivalTime :	#如果前面的抵達時間比較大 就前後交換
				ans[j], ans[j+1] = ans[j+1], ans[j]
			elif ans[j].ArrivalTime == ans[j+1].ArrivalTime :	#如果抵達時間一樣
				if ans[j].ID > ans[j+1].ID :					#如果前面ID比較大
					ans[j], ans[j+1] = ans[j+1], ans[j]			#交換

		
	return ans
	
def PSJFburst(mission3) :			#給一個list回傳依照抵達時間排列好的list (+CPUBURST)
	n = len(mission3)
	ans = mission3.copy()
	for i in range(0, n-1) :
		for j in range(0, n-i-1) :
			if ans[j].ArrivalTime > ans[j+1].ArrivalTime :	#如果前面的抵達時間比較大 就前後交換
				ans[j], ans[j+1] = ans[j+1], ans[j]
			elif ans[j].ArrivalTime == ans[j+1].ArrivalTime :	#如果抵達時間一樣
				if ans[j].CPUburst > ans[j+1].CPUburst :		#如果前面BURST比較大
					ans[j], ans[j+1] = ans[j+1], ans[j]			#交換
	return ans 
	
def sortformission2( mission2, timer ) :	#只要呼叫他 代表有人TIMEOUT 要重新排程
											#把第一個人換到現在時間的最後一位(通常不是直接最後面)
											#回傳排好的lise
	n = len(mission2)
	ans = mission2.copy()
	ischange = False
	for i in range(1, n) :	#自己不用看
		if ans[i].ArrivalTime > timer :#如果下一個人比現在時間晚 就排在他前面 
			if i != 0 :
				ans.insert(i, ans[0])
				ans.pop(0)					
				ischange = True
				break
				
	if ischange == False :	#你要直接排到最後面
		ans.append(ans[0])
		ans.pop(0)
	
	return ans
	
def sortformission34( mission3, time ) :	#回傳依照剩餘工作時間排列好的list 沒使用過 抵達時間 ID(time之前才要排)
	n = -1					#n代表在ANS的ARRAY中前N個是排好的 因為在現在這個時間點前到了
	ans = mission3.copy()
	for i in range(len(ans)) :				#算有幾個人要換
		if ans[i].ArrivalTime <= time :
			n +=1 
	for i in range(n+1) :
		for j in range(n-i) :
			if  ans[j].CPUburst3 > ans[j+1].CPUburst3 :
				ans[j], ans[j+1] = ans[j+1], ans[j]
			elif ans[j].CPUburst3 == ans[j+1].CPUburst3 :
				#print(ans[j].ruse)
				if ans[j].isuse == 1 and ans[j+1].isuse == 0  :
					pass	#不知道為啥這樣才是正確答案  依照說明文件應該是
					#ans[j], ans[j+1] = ans[j+1], ans[j] #要交換才對
				else :		#前面沒用過後面用過 兩個都用過 兩個都沒用過
					if ans[j].ArrivalTime > ans[j+1].ArrivalTime :
						ans[j], ans[j+1] = ans[j+1], ans[j]
					elif ans[j].ArrivalTime == ans[j+1].ArrivalTime :
						if ans[j].ID < ans[j+1].ID :
							ans[j], ans[j+1] = ans[j+1], ans[j]
	
	return ans
	
def sortformission4( mission3, time ) :	#回傳依照剩餘工作時間排列好的list 沒使用過 抵達時間 ID(time之前才要排)
	n = -1					#n代表在ANS的ARRAY中前N個是排好的 因為在現在這個時間點前到了
	ans = mission3.copy()
	for i in range(len(ans)) :				#算有幾個人要換
		if ans[i].ArrivalTime <= time :
			n +=1 
	for i in range(n+1) :
		for j in range(n) :
			if  ans[j].CPUburst4 > ans[j+1].CPUburst4 :
				ans[j], ans[j+1] = ans[j+1], ans[j]
			elif ans[j].CPUburst4 == ans[j+1].CPUburst4 :
				#print(ans[j].ruse)
				if ans[j].isuse == 1 and ans[j+1].isuse == 0  :
					pass	#不知道為啥這樣才是正確答案  依照說明文件應該是
					#print(ans[j].ID)
					#print(ans[j+1].ID)
					#print("time", end = "")
					#print(time)
					#ans[j], ans[j+1] = ans[j+1], ans[j] #要交換才對
				else :		#前面沒用過後面用過 兩個都用過 兩個都沒用過
					if ans[j].ArrivalTime > ans[j+1].ArrivalTime :
						ans[j], ans[j+1] = ans[j+1], ans[j]
					elif ans[j].ArrivalTime == ans[j+1].ArrivalTime :
						if ans[j].ID < ans[j+1].ID :
							ans[j], ans[j+1] = ans[j+1], ans[j]
	
	return ans
	
def sortformission5( mission5, time ) :	#回傳依照priority的list 沒使用過 抵達時間 ID(time之前才要排)
	n = -1					#n代表在ANS的ARRAY中前N個是排好的 因為在現在這個時間點前到了
	ans = mission5.copy()
	for i in range(len(ans)) :				#算有幾個人要換
		if ans[i].ArrivalTime <= time :
			n +=1 
	for i in range(n+1) :					#前面有幾個人排好過
		ans[i].ischeck = True 
	for i in range(n+1) :
		for j in range(n-i) :
			################ans[j].ischeckornot = True
			################ans[j+1].ischeckornot = True
			if  ans[j].Priority > ans[j+1].Priority :
				ans[j], ans[j+1] = ans[j+1], ans[j]
			elif ans[j].Priority == ans[j+1].Priority :				#優先等級一樣 看有沒有用過.. 抵達時間.. ID
				if ans[j].isuse == 1 and ans[j+1].isuse == 0 :
					ans[j], ans[j+1] = ans[j+1], ans[j]
				elif ans[j].isuse == 0 and ans[j+1].isuse == 1 :
					pass
				else :		#兩個都用過 兩個都沒用過
					if ans[j].ArrivalTime > ans[j+1].ArrivalTime :
						ans[j], ans[j+1] = ans[j+1], ans[j]
					elif ans[j].ArrivalTime == ans[j+1].ArrivalTime :
						if ans[j].ID < ans[j+1].ID :
							ans[j], ans[j+1] = ans[j+1], ans[j]
	
	return ans
	
def anybodyarrival( mission, time ) :				#回傳這個TIME有沒有人到達
	for i in range(len(mission)) :
		if mission[i].ArrivalTime == time :
			if mission[i].rCheck :
				return True
				
	return False #出來代表這時間都沒人到達
	
def sortformission5for( mission5, time ) :	#回傳依照priority的list 沒使用過 抵達時間 ID(time之前才要排)
	n = -1					#n代表在ANS的ARRAY中前N個是排好的 因為在現在這個時間點前到了
	ans = mission5.copy()
	for i in range(len(ans)) :
		if ans[i].ArrivalTime <= time :
			n +=1 
	for i in range(n+1) :
		ans[i].ischeck = True 
	for i in range(n+1) :
		for j in range(n-i) :
			if  ans[j].Priority > ans[j+1].Priority :
				if ans[j].CPUburst5 != 0 :					#跟外面的不一樣 因為這裡可能CPUB已經是0還進這個大FUNCTION
					ans[j], ans[j+1] = ans[j+1], ans[j]		#所以要額外檢查如果第一個人如果==0就不要讓他跟第二個人交換
			elif ans[j].Priority == ans[j+1].Priority :
				if ans[j].isuse == 1 and ans[j+1].isuse == 0 :
					ans[j], ans[j+1] = ans[j+1], ans[j]
					#pass
				else :		#前面沒用過後面用過 兩個都用過 兩個都沒用過
					if ans[j].ArrivalTime > ans[j+1].ArrivalTime :
						ans[j], ans[j+1] = ans[j+1], ans[j]
					elif ans[j].ArrivalTime == ans[j+1].ArrivalTime :
						if ans[j].ID < ans[j+1].ID :
							ans[j], ans[j+1] = ans[j+1], ans[j]
	
	return ans

def findIDinmission( mission, ID ) :		#給一個ID名稱還有 mission 的array   回傳ID在ARRAY的位置
	for i in range(len(mission)) :
		if ID == mission[i].ID :
			return i 
	
def missionOne(mission1, timeslice) :
	ans = copy.copy(mission1)
	count = 0
	FCFSgan = []
	doneNum = len(ans)
	while doneNum != 0 :
		if count < ans[0].ArrivalTime :		#如果還沒人到要空的
			FCFSgan.append("-")
			count += 1
		else :
			while ans[0].CPUburst > 0 :
				FCFSgan.append(ans[0].ID)
				ans[0].CPUburst -= 1
				count += 1
			#turnaround 是做完時間-到達時間
			mission1[len(mission1)-len(ans)].turnaroundT(count-ans[0].ArrivalTime, 1)
			mission1[len(mission1)-len(ans)].waitT(mission1[len(mission1)-len(ans)].turnaroundtimeFCFS-mission1[len(mission1)-len(ans)].CPUburst2, 1)
			ans.pop(0)
			doneNum -= 1 
			
	mission1 = sortforID( mission1 )
	#for i in range(0, len(mission1)) :
		#print(mission1[i].turnaroundtimeFCFS)
		#print(mission1[i].waittimeFCFS)
	ggan = ""
	for i in range(len(FCFSgan)) :					#把他轉成正確的OUTPUT
		ggan = ggan + str(printans(FCFSgan[i]))
	#return FCFSgan
	#print(ggan)
	return ggan
	
def missionTwo(mission2, timeslice) :
	ans = copy.copy(mission2) 
	count = 0 #算timeslice
	RRgna = []
	doneNum = len(ans)
	timer = 0 #計時器
	ifsort = False #用來看是否重新排程
	while doneNum != 0 :
		if timer < ans[0].ArrivalTime : #如果都還沒有人來 就不做
			RRgna.append("-")
			timer += 1
		else :	#如果有人來 就做完TIME SLICE 提早做完要讓其他可以做的直接繼續 COUNT要歸零
				#如果做到 TIME 讓他排到最後面
			while count < timeslice :
				if ans[0].CPUburst2 > 0 :
					ans[0].CPUburst2 -= 1 
					RRgna.append(ans[0].ID)
					count += 1 
					timer += 1
					if ans[0].CPUburst2 == 0 and count == timeslice :	#剛好TIMESLICE時做完
						inwhere = findIDinmission(mission2, ans[0].ID)
						mission2[inwhere].turnaroundT(timer-ans[0].ArrivalTime, 2)
						mission2[inwhere].waitT(mission2[inwhere].turnaroundtimeRR-mission2[inwhere].CPUburst3, 2)
						ans.pop(0)
						doneNum -= 1
						ifsort = False 
					elif ans[0].CPUburst2 != 0 and count == timeslice :	#重新排程
						ifsort = True 
				else : #提早做完mission2[0].CPUburst2 = 0
					inwhere = findIDinmission(mission2, ans[0].ID)
					mission2[inwhere].turnaroundT(timer-ans[0].ArrivalTime, 2)
					mission2[inwhere].waitT(mission2[inwhere].turnaroundtimeRR-mission2[inwhere].CPUburst3, 2)
					ans.pop(0)
					count = 0
					doneNum -= 1
					break
			
			count = 0 
			#到這邊代表作完(不管提早還是TIMEOUT)
			if ifsort :
				ans = sortformission2(ans, timer)
				ifsort = False
				
	mission2 = sortforID( mission2 )
	#return RRgna
	ggan = ""
	for i in range(len(RRgna)) :
		ggan = ggan + str(printans(RRgna[i]))
	return ggan
	
def missionThr(mission3, timeslice)	:
	ans = copy.copy(mission3) 
	for n in range(len(ans)) :		#全部都設定為沒用過
		ans[n].isuseornot(0)
	ans = PSJFburst(ans)
	ans = sortformission34(ans, 0)	#先依照規則排過一次
	count = 0
	PSJFgan = []
	doneNum = len(ans)
	while doneNum != 0 :
		if count < ans[0].ArrivalTime :
			PSJFgan.append("-")
			count += 1
			ans = sortformission34(ans, count)
		else :
			while ans[0].CPUburst3 > 0 :
				PSJFgan.append(ans[0].ID)
				ans[0].CPUburst3 -= 1
				ans[0].isuseornot(1)	#記得要把他設定有進來CPU過
				count += 1
				ans = sortformission34(ans, count) 	#每秒做完都要檢查排程
			if ans[0].CPUburst3 == 0 :								#有人做完記得算WAIT TURNAROUND 再POP
				inwhere = findIDinmission(mission3, ans[0].ID)
				mission3[inwhere].turnaroundT(count-ans[0].ArrivalTime, 3)
				mission3[inwhere].waitT(mission3[inwhere].turnaroundtimePSJF-mission3[inwhere].CPUburst4, 3)
				ans.pop(0)
				ans = sortformission34(ans, count)
				doneNum -= 1 
				
	mission3 = sortforID( mission3 )
	#return PSJFgan
	ggan = ""
	for i in range(len(PSJFgan)) :
		ggan = ggan + str(printans(PSJFgan[i]))
	return ggan
	
def missionFou(mission4, timeslice)	:	#3和4的差別只有重新排程的時機點不一樣
	ans = copy.copy(mission4) 
	for n in range(len(ans)) :		#全部都設定為沒用過
		ans[n].isuseornot(0)
	ans = PSJFburst(ans)
	ans = sortformission4(ans, 0)	#先依照規則排過一次
	count = 0
	NSJFgan = []
	doneNum = len(ans)
	while doneNum != 0 :
		if count < ans[0].ArrivalTime :
			NSJFgan.append("-")
			count += 1
			ans = sortformission4(ans, count)
		else :
			while ans[0].CPUburst4 > 0 :
				NSJFgan.append(ans[0].ID)
				ans[0].CPUburst4 -= 1
				ans[0].isuse = 1	#記得要把他設定有進來CPU過
				count += 1
				#ans = sortformission4(ans, count) 
			if ans[0].CPUburst4 == 0 :
				inwhere = findIDinmission(mission4, ans[0].ID)
				mission4[inwhere].turnaroundT(count-ans[0].ArrivalTime, 4)
				mission4[inwhere].waitT(mission4[inwhere].turnaroundtimeNPSJF-mission4[inwhere].CPUburst5, 4)
				ans.pop(0)
				ans = sortformission4(ans, count) 	#有人完全做完再檢查排程
				doneNum -= 1 
	
	mission4 = sortforID( mission4 )
	#return NSJFgan
	ggan = ""
	for i in range(len(NSJFgan)) :
		ggan = ggan + str(printans(NSJFgan[i]))
	return ggan

def missionFIV(mission5, timeslice)	:
	ans = copy.copy(mission5) 
	for n in range(len(ans)) :		#全部都設定為沒用過
		ans[n].isuseornot(0)
	for n in range(len(ans)) :
		ans[n].ischeckornot = 0 
	ans = sortformission5(ans, 0)	#先依照規則排過一次
	count = 0
	PPgan = []
	doneNum = len(ans)
	while doneNum != 0 :
		if count < ans[0].ArrivalTime :
			PPgan.append("-")
			count += 1
			ans = sortformission5(ans, count)
		else :
			while ans[0].CPUburst5 > 0 :
				PPgan.append(ans[0].ID)				
				ans[0].CPUburst5 -= 1
				ans[0].isuseornot(1)	#記得要把他設定有進來CPU過
				#if ans[0].CPUburst5 == 0 :
					#break
				count += 1
				if anybodyarrival(ans, count) :			#有人到達就要檢查排程
					ans = sortformission5for(ans, count)	#正在跑的CPU跟後面比 如果就算優先一樣 但是沒用過就不會被搶奪
				#if ggg ==2 表示明明是CPU已經結束了但卻被換掉
			if ans[0].CPUburst5 == 0 :
				inwhere = findIDinmission(mission5, ans[0].ID)
				#if ans[0].ID == 9 :
				#	mission5[inwhere].turnaroundT(count-ans[0].ArrivalTime-1, 5)
				#else :
				mission5[inwhere].turnaroundT(count-ans[0].ArrivalTime, 5)
				#if ans[0].ID == 9 :
					#print(count)
					#print(ans[0].ArrivalTime)
					#print(mission5[inwhere].turnaroundtimePRIORITY)
				mission5[inwhere].waitT(mission5[inwhere].turnaroundtimePRIORITY-mission5[inwhere].CPUburst6, 5)
				#if ans[0].ID == 9 :
					#print(count)
				ans.pop(0)
				ans = sortformission5(ans, count) 	#有人做完就要檢查
				doneNum -= 1 
			
		#print(count)
		#print(PPgan)
	mission5 = sortforID( mission5 )
	#return PPgan
	ggan = ""
	for i in range(len(PPgan)) :
		ggan = ggan + str(printans(PPgan[i]))
	return ggan

def printans(gan) :
	ch = ''
	if gan == '-' :
		ch = '-'
	elif gan < 10 :
		return gan
	elif gan == 10 :
		ch = 'A'
	elif gan == 11 :
		ch = 'B'
	elif gan == 12 :
		ch = 'C'
	elif gan == 13 :
		ch = 'D'
	elif gan == 14 :
		ch = 'E'
	elif gan == 15 :
		ch = 'F'
	elif gan == 16 :
		ch = 'G'
	elif gan == 17 :
		ch = 'H'
	elif gan == 18 :
		ch = 'I'
	elif gan == 19 :
		ch = 'J'
	elif gan == 20 :
		ch = 'K'
	elif gan == 21 :
		ch = 'L'
	elif gan == 22 :
		ch = 'M'
	elif gan == 23 :
		ch = 'N' 
	elif gan == 24 :
		ch = 'O' 
	elif gan == 25 :
		ch = 'P'
	elif gan == 26 :
		ch = 'Q'
	elif gan == 27 :
		ch = 'R' 
	elif gan == 28 :
		ch = 'S'
	elif gan == 29 :
		ch = 'T'
	elif gan == 30 :
		ch = 'U'
	elif gan == 31 :
		ch = 'V'
	elif gan == 32 :
		ch = 'W'
	elif gan == 33 :
		ch = 'X'
	elif gan == 34 :
		ch = 'Y'
	elif gan == 35 :
		ch = 'Z'
			
	return ch
		
if __name__=='__main__' :
	filename = input("輸入input檔名(單獨一個0結束):" )
	while filename != '0' :
		filenamereade = filename + '.txt' #完整檔名
		file = open(filenamereade,'r') #開黨
		worklist = [] #工作地方
		star = []
		#讀取第一行
		tempinput = file.readline()
		star = tempinput.split()
		whichmission = int(star[0]) #要做哪一個項目
		timeslice = int(star[1])	#要做的時間間隔
		"""print("whichmission:", end = "" )
		print(whichmission) 			 
		print("timeslice:", end = "" )
		print(timeslice) """			
		
		tempinput = file.readline() #讀掉沒用的
		allinput = file.read() #讀全部的資料
		worklist = allinput.split('\n') #資料處理
		if worklist[len(worklist)-1] == '':		#如果最後面有空行要刪掉保持資料裡面的完整
			worklist.pop()
		#print("worklist:", end = "" )
		#print(worklist)
		cleanlist = []
		for n in range(0, len(worklist)) :
			tArray = worklist[n].split()
			cleanlist.append(Process(tArray[0], tArray[1], tArray[2], tArray[3]))
		
		
		mission1 = FCFSarrival( cleanlist )
		#print("mission1:" )
		"""gg = 0 
		while gg in range(len(mission1)) : #檢查有沒有順序排對
			print(mission1[gg].ID, end = "	")
			print(mission1[gg].CPUburst, end = "	")
			print(mission1[gg].ArrivalTime, end = "	")
			print(mission1[gg].Priority)
			gg+=1
		
		gg = 0"""
		mission2 = copy.copy(mission1)		#每個人的LIST要不一樣 因為會被POP
		mission3 = copy.copy(mission1)
		mission4 = copy.copy(mission1)
		mission5 = copy.copy(mission1)
		mis1gan = "\n"
		mis2gan = "\n"
		mis3gan = "\n"
		mis4gan = "\n"
		mis5gan = "\n"
		if whichmission == 1 :
			#print("FCFS")
			mis1gan = missionOne(mission1, timeslice)
			print("mis1 DONE!")
		elif whichmission == 2 :
			#print("RR")
			mis2gan = missionTwo(mission2, timeslice)
			print("mis2 DONE!")
		elif whichmission == 3 :
			#print("PSJF")
			mis3gan = missionThr(mission3, timeslice)
			print("mis3 DONE!")
		elif whichmission == 4 :
			#print("Non-PSJF")
			mis4gan = missionFou(mission4, timeslice)
			print("mis4 DONE!")
		elif whichmission == 5 :
			#print("Priority")
			mis5gan = missionFIV(mission5, timeslice)
			print("mis5 DONE!")
		elif whichmission == 6 :
			#print("FCFS")
			mis1gan = missionOne(mission1, timeslice)
			#print("RR")
			mis2gan = missionTwo(mission2, timeslice)
			#print("PSJF")
			mis3gan = missionThr(mission3, timeslice)
			#print("Non-PSJF")
			mis4gan = missionFou(mission4, timeslice)
			#print("Priority")
			mis5gan = missionFIV(mission5, timeslice)
			print("mis6 DONE!")
		
		mission1 = sortforID( mission1 )		#按照ID大小列出來
		mission2 = sortforID( mission2 )
		mission3 = sortforID( mission3 )
		mission4 = sortforID( mission4 )
		mission5 = sortforID( mission5 )
		filenamewrite = filename + "_output.txt" 		#寫檔案 依照哪一個任務決定要不要做
		filewrite = open(filenamewrite,'w')
		if whichmission == 1 or whichmission == 6 :
			filewrite.write("FCFS\n")
			filewrite.write(mis1gan)
		if whichmission == 2 or whichmission == 6 :
			filewrite.write("\nRR\n")
			filewrite.write(mis2gan)
		if whichmission == 3 or whichmission == 6 :
			filewrite.write("\nPSJF\n")
			filewrite.write(mis3gan)
		if whichmission == 4 or whichmission == 6 :
			filewrite.write("\nNSJF\n")
			filewrite.write(mis4gan)
		if whichmission == 5 or whichmission == 6 :
			filewrite.write("\nPriority\n")
			filewrite.write(mis5gan)
		filewrite.write("\n"+"=========================================")
		filewrite.write("\n"+"Waiting Time")
		filewrite.write("\n"+"ID	FCFS	RR	PSJF	NSJF	PRIORITY")
		for i in range(0, len(mission1)) :
			#print(mission1[i].ID)
			filewrite.write("\n"+str(mission1[i].ID) + "	")
			if whichmission == 1 or whichmission == 6 :
				filewrite.write(str(mission1[i].waittimeFCFS) + "	")
			if whichmission == 2 or whichmission == 6 :
				filewrite.write(str(mission2[i].waittimeRR) + "	")
			if whichmission == 3 or whichmission == 6 :
				filewrite.write(str(mission3[i].waittimePSJF) + "	")
			if whichmission == 4 or whichmission == 6 :
				filewrite.write(str(mission4[i].waittimeNPSJF) + "	")
			if whichmission == 5 or whichmission == 6 :
				filewrite.write(str(mission5[i].waittimePRIORITY) + "\n")
		filewrite.write("\n"+"=========================================")
		filewrite.write("\n"+"Turnaround Time")
		filewrite.write("\n"+"ID	FCFS	RR	PSJF	NSJF	PRIORITY")
		for i in range(len(mission1)) :
			filewrite.write("\n"+str(mission1[i].ID) + "	")
			if whichmission == 1 or whichmission == 6 :
				filewrite.write(str(mission1[i].turnaroundtimeFCFS) + "	")
			if whichmission == 2 or whichmission == 6 :
				filewrite.write(str(mission2[i].turnaroundtimeRR) + "	")
			if whichmission == 3 or whichmission == 6 :
				filewrite.write(str(mission3[i].turnaroundtimePSJF) + "	")
			if whichmission == 4 or whichmission == 6 :
				filewrite.write(str(mission4[i].turnaroundtimeNPSJF) + "	")
			if whichmission == 5 or whichmission == 6 :
				filewrite.write(str(mission5[i].turnaroundtimePRIORITY) + "\n")
		filewrite.close()
		"""print("===============================================")
		print("Waiting Time")
		print("ID	FCFS	RR	PSJF	NSJF	PRIORITY")
		for i in range(len(mission1)) :
			print(mission1[i].ID, end="	")
			print(mission1[i].waittimeFCFS, end="	")
			print(mission2[i].waittimeRR, end="	")
			print(mission3[i].waittimePSJF, end="	")
			print(mission4[i].waittimeNPSJF, end="	")
			print(mission5[i].waittimePRIORITY)
		
		print("===============================================")
		print("Turnaround Time")
		print("ID	FCFS	RR	PSJF	NSJF	PRIORITY")
		for i in range(len(mission1)) :
			print(mission1[i].ID, end="	")
			print(mission1[i].turnaroundtimeFCFS, end="	")
			print(mission2[i].turnaroundtimeRR, end="	")
			print(mission3[i].turnaroundtimePSJF, end="	")
			print(mission4[i].turnaroundtimeNPSJF, end="	")
			print(mission5[i].turnaroundtimePRIORITY)"""
			
		"""print("CL:")			#測試看裡面的資料
		print(len(cleanlist))
		count = 0
		while count < len(cleanlist) :
			print(count)
			print("ID")
			print(cleanlist[count].ID)
			print("CPUburst")
			print(cleanlist[count].CPUburst)
			print("ArrivalTime")
			print(cleanlist[count].ArrivalTime)
			print("Priority")
			print(cleanlist[count].Priority)
			count +=1
		
		count = 0"""
		
		#writeoutput(worklist, end - star, filename) #寫檔案出來
		file.close() #關掉檔案
		#下面都是初始化
		timeslice = 0
		whichmission = 0
		star = []
		worklist = []
		cleanlist = []
		
		filename = input("輸入input檔名(單獨一個0結束):" )
	#endwhile
#endif