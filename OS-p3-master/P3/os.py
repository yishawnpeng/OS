#10527142

class ShiftRegister :	#MIS3的data struct
	def __init__(self) :
		self.sr = "00000000"

def mission1(filename, page, filewrite) :
	pagenum = filename
	pagerefer = list(page)
	#print(pagerefer)
	print("FIFO")
	filewrite.write("FIFO\n")
	worklist = []
	pagefault = 0
	pagerepalce = 0
	while len(pagerefer) > 0 :
		now = pagerefer.pop(0)
		if len(worklist) == 0 :		#一開始是空的
			worklist.append(now)
			printact(now, worklist, 1, filewrite)
			pagefault += 1
		else :
			a = findpage(worklist, now)
			if a == -1 :	#這個人不在list裡面 又分為有滿還有沒滿
				pagefault += 1
				if len(worklist) != int(pagenum) :	#LIST沒滿
					worklist.insert(0, now)
					printact(now, worklist, 1, filewrite)
				elif len(worklist) == int(pagenum) :
					worklist.pop()
					pagerepalce += 1
					worklist.insert(0, now)
					printact(now, worklist, 1, filewrite)
			else :			#這個人在LIST裡面
				printact(now, worklist, 0, filewrite)

	print("Page Fault = ", pagefault, "	Page Repalce = ", pagerepalce, "	Page Frame = ", pagenum)
	filewrite.write("Page Fault = " + str(pagefault) + "	Page Repalce = " + str(pagerepalce) + "	Page Frame = " + str(pagenum))

	
def mission2(filename, page, filewrite) :
	pagenum = filename
	pagerefer = list(page)
	#print(pagerefer)
	print("LRU")
	filewrite.write("\nLRU\n")
	worklist = []
	pagefault = 0
	pagerepalce = 0
	while len(pagerefer) > 0 :
		now = pagerefer.pop(0)
		if len(worklist) == 0 :		#一開始是空的
			worklist.append(now)
			printact(now, worklist, 1, filewrite)
			pagefault += 1
		else :
			a = findpage(worklist, now)
			if a == -1 :	#這個人不在list裡面 又分為有滿還有沒滿
				pagefault += 1
				if len(worklist) != int(pagenum) :	#LIST沒滿
					worklist.insert(0, now)
					printact(now, worklist, 1, filewrite)
				elif len(worklist) == int(pagenum) :
					worklist.pop()
					pagerepalce += 1
					worklist.insert(0, now)
					printact(now, worklist, 1, filewrite)
			else :			#這個人在LIST裡面
				worklist.pop(a)
				worklist.insert(0, now)
				printact(now, worklist, 0, filewrite)

	print("Page Fault = ", pagefault, "	Page Repalce = ", pagerepalce, "	Page Frame = ", pagenum)
	filewrite.write("Page Fault = " + str(pagefault) + "	Page Repalce = " + str(pagerepalce) + "	Page Frame = " + str(pagenum))


def mission3(filename, page, filewrite) :
	pagenum = filename
	pagerefer = list(page)
	#print(pagerefer)
	print("Additional Reference Bits")
	filewrite.write("\nAdditional Reference Bits\n")
	worklist = []
	pagefault = 0
	pagerepalce = 0
	shiftregister = []
	for i in range(int(pagenum)) :
		shiftregister.append(ShiftRegister())
	#for i in range(int(pagenum)) :
		#print(i)
		#print(shiftregister[i].sr)
	while len(pagerefer) > 0 :
		now = pagerefer.pop(0)
		if len(worklist) == 0 :		#一開始是空的
			worklist.append(now)
			printact(now, worklist, 1, filewrite)
			pagefault += 1
			#shiftregister[0].sr.pop()
			shiftregister[0].sr = shiftregister[0].sr[:-1]
			#shiftregister[0].sr.insert(0, "1")
			shiftregister[0].sr = "1" + shiftregister[0].sr
			#print(shiftregister[0].sr)
		else :
			a = findpage(worklist, now)
			if a == -1 :	#這個人不在list裡面 又分為有滿還有沒滿
				pagefault += 1
				if len(worklist) != int(pagenum) :	#LIST沒滿
					worklist.insert(0, now)
					if len(worklist) != 1 :			#每個人往後搬
						for i in range(len(worklist)-1, 0) :
							shiftregister[i].sr = shiftregister[i-1].sr 
					for i in range(len(worklist)) :	#每個人都要SHIFH 新進的第一個式1 其他都0
						shiftregister[i].sr = shiftregister[i].sr[:-1]
						if i != 0 :
							shiftregister[i].sr = "0" + shiftregister[i].sr
						else :
							shiftregister[i].sr = "1" + shiftregister[i].sr
					
					printact(now, worklist, 1, filewrite)
				elif len(worklist) == int(pagenum) :
					where = findminsr(shiftregister)
					worklist.pop(where)
					worklist.insert(where, now)
					for i in range(len(worklist)) :	#每個人都要SHIFH 他自己第一個1 其他都0
						shiftregister[i].sr = shiftregister[i].sr[:-1]
						if i != where :
							shiftregister[i].sr = "0" + shiftregister[i].sr
						else : #新的不知道是不是10000000
							shiftregister[i].sr = "1" + shiftregister[i].sr
					pagerepalce += 1
					printact(now, worklist, 1, filewrite)
			else :			#這個人在LIST裡面
				#worklist.pop(a)
				#worklist.insert(0, now)
				printact(now, worklist, 0, filewrite)
				for i in range(len(worklist)) :	#每個人都要SHIFH 他自己第一個1 其他都0
					shiftregister[i].sr = shiftregister[i].sr[:-1]
					if i != a :
						shiftregister[i].sr = "0" + shiftregister[i].sr
					else :
						shiftregister[i].sr = "1" + shiftregister[i].sr
				#shiftregister[a].sr = shiftregister[a].sr[:-1]
				#shiftregister[a].sr = "1" + shiftregister[a].sr
				

	print("Page Fault = ", pagefault, "	Page Repalce = ", pagerepalce, "	Page Frame = ", pagenum)
	filewrite.write("Page Fault = " + str(pagefault) + "	Page Repalce = " + str(pagerepalce) + "	Page Frame = " + str(pagenum))


def mission4(filename, page, filewrite) :
	pagenum = filename
	pagerefer = list(page)
	#print(pagerefer)
	print("Second Chance Page")
	filewrite.write("\nSecond Chance Page\n")
	worklist = []
	pagefault = 0
	pagerepalce = 0
	referencebitlist = []
	while len(pagerefer) > 0 :
		now = pagerefer.pop(0)
		if len(worklist) == 0 :		#一開始是空的
			worklist.append(now)
			referencebitlist.append(1)
			#print(type(referencebitlist[0]))
			printact(now, worklist, 1, filewrite)
			pagefault += 1
		else :
			a = findpage(worklist, now)
			if a == -1 :	#這個人不在list裡面 又分為有滿還有沒滿
				pagefault += 1
				if len(worklist) != int(pagenum) :	#LIST沒滿
					worklist.insert(0, now)
					referencebitlist.insert(0, 1)
					printact(now, worklist, 1, filewrite)
				elif len(worklist) == int(pagenum) :
					changewho = -1
					for i in range(len(referencebitlist)) :	#找人換 找到最後一個0
						if referencebitlist[i] == 0 :
							changewho = i
					#if now == "0" :
						#print("*")
						#print(changewho)
					
					if changewho == -1 :	#還是-1就代表每個人都是1 要換最後一個人	
						for i in range(len(referencebitlist)) :	#每個人都是0
							referencebitlist[i] = 0
						referencebitlist[0] = 1	#第一個人改1
						#print(worklist[len(worklist)-1])
						worklist.pop()
						worklist.insert(0, now)
						pagerepalce += 1
						printact(now, worklist, 1, filewrite)
						#print(referencebitlist[0], referencebitlist[1], referencebitlist[2], "++")
					else :
						#看最後一人是不是0 不是的話改成0放到最前面
						#直到最後一個人0
						#就把他丟掉 拿新的進來
						while referencebitlist[len(referencebitlist)-1] == 1 :
							tempW = worklist.pop()
							twmpR = referencebitlist.pop()
							referencebitlist.insert(0, 0)
							worklist.insert(0, tempW)
						###出來代表最後一個人0
						worklist.pop()
						referencebitlist.pop()
						worklist.insert(0, now)
						#for i in range(len(referencebitlist)) :	#每個人都是0
							#referencebitlist[i] = 0
						referencebitlist.insert(0, 1)
						pagerepalce += 1
						printact(now, worklist, 1, filewrite)
			else :			#這個人在LIST裡面
				"""worklist.pop(a)
				referencebitlist.pop(a)
				worklist.insert(0, now)
				referencebitlist.insert(0, 1)"""
				#for i in range(len(referencebitlist)) :	#每個人都是0
					#referencebitlist[i] = 0
				referencebitlist[a] = 1
				printact(now, worklist, 0, filewrite)
				#print(referencebitlist[0], referencebitlist[1], referencebitlist[2], "++")

	print("Page Fault = ", pagefault, "	Page Repalce = ", pagerepalce, "	Page Frame = ", pagenum)
	filewrite.write("Page Fault = " + str(pagefault) + "	Page Repalce = " + str(pagerepalce) + "	Page Frame = " + str(pagenum))


def mission5(filename, page, filewrite) :
	pagenum = filename
	pagerefer = list(page)
	#print(pagerefer)
	print("Least Frequently Used Page Replacement")
	filewrite.write("\nLeast Frequently Used Page Replacement\n")
	worklist = []
	pagefault = 0
	pagerepalce = 0
	leastfrequentlyusedlist = []
	while len(pagerefer) > 0 :
		now = pagerefer.pop(0)
		if len(worklist) == 0 :		#一開始是空的
			worklist.append(now)
			leastfrequentlyusedlist.append(0)
			printact(now, worklist, 1, filewrite)
			pagefault += 1
		else :
			a = findpage(worklist, now)
			if a == -1 :	#這個人不在list裡面 又分為有滿還有沒滿
				pagefault += 1
				if len(worklist) != int(pagenum) :	#LIST沒滿
					worklist.insert(0, now)
					leastfrequentlyusedlist.insert(0, 0)
					printact(now, worklist, 1, filewrite)
				elif len(worklist) == int(pagenum) :
					#changewho = -1
					changewho = findminF(leastfrequentlyusedlist)
					worklist.pop(changewho)
					leastfrequentlyusedlist.pop(changewho)
					worklist.insert(0, now)
					leastfrequentlyusedlist.insert(0, 0)
					pagerepalce += 1
					printact(now, worklist, 1, filewrite)
					"""for i in range(len(leastfrequentlyusedlist)) :	#找人換 找到最後一個0
						if leastfrequentlyusedlist[i] == 0 :
							changewho = i
					if changewho == -1 :	#還是-1就代表每個人都是1 要換最後一個人	
						for i in range(len(leastfrequentlyusedlist)) :	#每個人都是0
							leastfrequentlyusedlist[i] = 0
						leastfrequentlyusedlist[0] = 1	#第一個人改1
						worklist.pop()
						worklist.insert(0, now)
						pagerepalce += 1
						printact(now, worklist, 1)
					else :	#有找到最後一個0 換掉他
						worklist.pop(changewho)
						leastfrequentlyusedlist.pop(changewho)
						worklist.insert(0, now)
						leastfrequentlyusedlist.insert(0, 1)
						pagerepalce += 1
						printact(now, worklist, 1)"""
			else :			#這個人在LIST裡面
				"""if leastfrequentlyusedlist[a] == 0 :
					worklist.pop(a)
					temp = leastfrequentlyusedlist.pop(a)
					worklist.insert(0, now)
					leastfrequentlyusedlist.insert(0, temp+1)"""
				#else :
				leastfrequentlyusedlist[a] = leastfrequentlyusedlist[a] + 1
				"""leastfrequentlyusedlist[a] += 1
				#worklist.pop(a)
				#worklist.insert(0, now)"""
				printact(now, worklist, 0, filewrite)

	print("Page Fault = ", pagefault, "	Page Repalce = ", pagerepalce, "	Page Frame = ", pagenum)
	filewrite.write("Page Fault = " + str(pagefault) + "	Page Repalce = " + str(pagerepalce) + "	Page Frame = " + str(pagenum))



def mission6(filename, page, filewrite) :
	pagenum = filename
	pagerefer = list(page)
	#print(pagerefer)
	print("Most Frequently Used Page Replacement")
	filewrite.write("\nMost Frequently Used Page Replacement\n")
	worklist = []
	pagefault = 0
	pagerepalce = 0
	leastfrequentlyusedlist = []
	while len(pagerefer) > 0 :
		now = pagerefer.pop(0)
		if len(worklist) == 0 :		#一開始是空的
			worklist.append(now)
			leastfrequentlyusedlist.append(0)
			printact(now, worklist, 1, filewrite)
			pagefault += 1
		else :
			a = findpage(worklist, now)
			if a == -1 :	#這個人不在list裡面 又分為有滿還有沒滿
				pagefault += 1
				if len(worklist) != int(pagenum) :	#LIST沒滿
					worklist.insert(0, now)
					leastfrequentlyusedlist.insert(0, 0)
					printact(now, worklist, 1, filewrite)
				elif len(worklist) == int(pagenum) :
					#changewho = -1
					changewho = findmaxF(leastfrequentlyusedlist)
					worklist.pop(changewho)
					leastfrequentlyusedlist.pop(changewho)
					worklist.insert(0, now)
					leastfrequentlyusedlist.insert(0, 0)
					pagerepalce += 1
					printact(now, worklist, 1, filewrite)
					"""for i in range(len(leastfrequentlyusedlist)) :	#找人換 找到最後一個0
						if leastfrequentlyusedlist[i] == 0 :
							changewho = i
					if changewho == -1 :	#還是-1就代表每個人都是1 要換最後一個人	
						for i in range(len(leastfrequentlyusedlist)) :	#每個人都是0
							leastfrequentlyusedlist[i] = 0
						leastfrequentlyusedlist[0] = 1	#第一個人改1
						worklist.pop()
						worklist.insert(0, now)
						pagerepalce += 1
						printact(now, worklist, 1)
					else :	#有找到最後一個0 換掉他
						worklist.pop(changewho)
						leastfrequentlyusedlist.pop(changewho)
						worklist.insert(0, now)
						leastfrequentlyusedlist.insert(0, 1)
						pagerepalce += 1
						printact(now, worklist, 1)"""
			else :			#這個人在LIST裡面
				"""if leastfrequentlyusedlist[a] == 0 :
					worklist.pop(a)
					temp = leastfrequentlyusedlist.pop(a)
					worklist.insert(0, now)
					leastfrequentlyusedlist.insert(0, temp+1)"""
				#else :
				leastfrequentlyusedlist[a] = leastfrequentlyusedlist[a] +1
				
				"""leastfrequentlyusedlist[a] += 1
				#worklist.pop(a)
				#worklist.insert(0, now)"""
				printact(now, worklist, 0, filewrite)

	print("Page Fault = ", pagefault, "	Page Repalce = ", pagerepalce, "	Page Frame = ", pagenum)
	filewrite.write("Page Fault = " + str(pagefault) + "	Page Repalce = " + str(pagerepalce) + "	Page Frame = " + str(pagenum))

def findminsr(shiftregister) :
	"""print("star")
	for i in range(len(shiftregister)) :
		print(shiftregister[i].sr)
	print("end")"""
	a = "11111111"
	wh = -1
	for i in range(len(shiftregister)) :
		if shiftregister[i].sr <= a :
			wh = i 
			a = shiftregister[i].sr
			
	#print(wh)
	#print(a)
	return wh
	
def findminF(leastfrequentlyusedlist) :	#任務五找最小的數字 
	a = 10000
	wh = -1
	for i in range(len(leastfrequentlyusedlist)) :
		if leastfrequentlyusedlist[i] <= a :	#第二組測試數據 一樣要把晚進的幹掉
			wh = i 
			a = leastfrequentlyusedlist[i]
			
	return wh
	
def findmaxF(leastfrequentlyusedlist) :	#任務六找最大的數字
	a = -1
	wh = -1
	for i in range(len(leastfrequentlyusedlist)) :
		if leastfrequentlyusedlist[i] >= a :
			wh = i 
			a = leastfrequentlyusedlist[i]
			
	return wh
	
def printact(nowpage, worklist, isF, filewrite ) :
	print(nowpage, end="	")
	filewrite.write(nowpage + "	" )
	for i in range(len(worklist)) :
		print(worklist[i],end="")
		filewrite.write(worklist[i])
		
	print("		", end="")
	filewrite.write("	")
	if isF == 1 :
		print("F")
		filewrite.write("F\n")
	else :
		print("	")
		filewrite.write("\n")

		
def findpage(worklist, name) :
	for i in range(len(worklist)) :
		if worklist[i] == name :
			return i 
			
	return -1

if __name__ == "__main__" :
	filename = input("請輸入input(單獨一個0結束):")
	while filename != "0" :
		
		filenamereade = filename + '.txt' #完整檔名
		file = open(filenamereade,'r') #開黨
		worklist = [] #工作地方
		#讀取第一行
		tempinput = file.readline()	
		page = file.readline()
		if page[-1] == '\n':		#刪掉最後的空格
			page = page[:-1]
			
		#page = page.rsplit()
		
		# page = input("請輸入Page:")
		
		filenamewrite = filename + "_output.txt" 		#寫檔案 依照哪一個任務決定要不要做
		filewrite = open(filenamewrite,'w')
		
		mission1(tempinput, page, filewrite)
		mission2(tempinput, page, filewrite)
		mission3(tempinput, page, filewrite)
		mission4(tempinput, page, filewrite)
		mission5(tempinput, page, filewrite)
		mission6(tempinput, page, filewrite)
		
		filewrite.close()
		
		
		filename = input("請輸入input(單獨一個0結束):")