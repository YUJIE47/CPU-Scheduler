import os
import time 
import queue
import threading as td
import multiprocessing as mp
from time import perf_counter


def Split_File(source_input, splitNum):
    '''split data into k part'''
    dataSize = len(source_input) // splitNum
    seperate_list = [source_input[i:i + dataSize] for i in range(0, dataSize * splitNum, dataSize)]
    seperate_list[splitNum - 1].extend(source_input[dataSize * splitNum:len(source_input)])
    return seperate_list


def BubbleSort(source_input, sorted):
    '''bubble sort, return queue'''
    for i in range(len(source_input)):
        for j in range(0, len(source_input)-i-1):
            if (source_input[j]) > (source_input[j + 1]):
                temp = source_input[j]
                source_input[j] = source_input[j+1]
                source_input[j+1] = temp
    
    sorted.put(source_input)


def BubbleSort_MT(source_input):
    '''for multiiprocessing, bubble sort, return list'''
    
    for i in range(len(source_input)):
        for j in range(0, len(source_input)-i-1):
            if (source_input[j]) > (source_input[j + 1]):
                temp = source_input[j]
                source_input[j] = source_input[j+1]
                source_input[j+1] = temp
    
    return source_input


def Merge(left, right, que):
    result = []
    while len(left) and len(right):
        if ( left[0] <= right[0] ):
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
            
    while len(left):          # leftArray 還沒排完
        result.append(left.pop(0)) 
    while len(right):         # rightArray 還沒排完
        result.append(right.pop(0)) 
    
    que.put(result)           # put the sorted list into the queue


def BubbleAndMerge(seperate_list, sorted):
    ''' For problem2
    First do bubble sort for k data, then do merge sort'''
    for i in seperate_list:
        BubbleSort(i, sorted)


    while sorted.qsize() != 1:
        leftArray = sorted.get()
        rightArray = sorted.get()
            
        Merge(leftArray, rightArray, sorted)
      

def WriteFile(inputname, program, list, cputime):
    filename = inputname + "_output" + program + ".txt"
    file = open(filename, "w")
    for i in list:
        file.write(str(i) + "\n")

    file.write("CPU Time : " + str(cputime) + "\n")
    date = time.asctime(time.localtime(time.time()))
    file.write("datetime : " + date)

    file.close() 


# -----------------------------------------------------------------------------------------------------

def Mission1(filename):
    '''Just do bubble sort'''
    full_filename = filename + ".txt"
    file_exist = False 
    try:
        file = open(full_filename, "r")
        file_exist = True
    except FileNotFoundError:
        print("Sorry! The file "+full_filename+" can't find.")

    if file_exist:
        source_input = file.read().split()
        source_to_int = list(map(int, source_input))
        file.close()

        t1_start = perf_counter() # timer
        sorted = queue.Queue()
        BubbleSort(source_to_int, sorted)

        t1_stop = perf_counter()  # timer
        cputime = t1_stop - t1_start
        print("CPU Time:", cputime)
        WriteFile(filename, "1", sorted.get(), cputime)
    

def Mission2(filename):
    '''Create a process, in this process complete bubble sort and merge sort
       bubble sort need to split k parts'''
    splitNum = input("請輸入要切成幾份:")
    full_filename = filename + ".txt" 
    file_exist = False 
    try:
        file = open(full_filename, "r")
        file_exist = True
    except FileNotFoundError:
        print("Sorry! The file "+full_filename+" can't find.")

    if file_exist:   
        source_input = file.read().split()
        source_to_int = list(map(int, source_input))
        file.close()

        seperate_list = Split_File(source_to_int, int(splitNum))
    
        manager = mp.Manager() # Create a manager object
        sorted_manager = manager.Queue()
        process1 = mp.Process(target=BubbleAndMerge, args=(seperate_list, sorted_manager))
        t1_start = perf_counter()

        process1.start()
        process1.join()

        t1_stop = perf_counter() 
        cputime = t1_stop - t1_start
        print("CPU Time:", cputime)
        WriteFile(filename, "2", sorted_manager.get(), cputime)
 

def Mission3(filename):
    splitNum = input("請輸入要切成幾份:")
    full_filename = filename + ".txt"
    file_exist = False
    try:
        file = open(full_filename, "r")
        file_exist = True
    except FileNotFoundError:
        print("Sorry! The file "+full_filename+" can't find.")

    if file_exist:
        source_input = file.read().split()
        source_to_int = list(map(int, source_input)) # Convert all input data from str to int
        file.close()

        seperate_list = Split_File(source_to_int, int(splitNum)) # Split data into k part

        t1_start = perf_counter() # timer

        cpuCount = os.cpu_count() 
        pool = mp.Pool(cpuCount)
        pool_outputs = pool.map(BubbleSort_MT, [i for i in seperate_list])
    

        manager = mp.Manager() # Create a manager object
        sorted = manager.Queue()

        for i in pool_outputs: # Convert bubble sort's output(list) to queue
            sorted.put(i)

        merge_process_list = []   
        for i in range(int(splitNum)-1):
            left = sorted.get()
            right = sorted.get()
            merge_process_list.append(mp.Process(target=Merge, args=(left, right, sorted)))
            merge_process_list[i].start()
            print("start process", i, '\n\n') # for testing

        for i in range(int(splitNum)-1):       
            merge_process_list[i].join()

        t1_stop = perf_counter() # timer
        cputime = t1_stop - t1_start
        print("CPU Time:", cputime)
        WriteFile(filename, "3", sorted.get(), cputime)


def Mission4(filename):
    splitNum = input("請輸入要切成幾份:")
    full_filename = filename + ".txt"
    file_exist = False
    try:
        file = open(full_filename, "r")
        file_exist = True
    except FileNotFoundError:
        print("Sorry! The file "+full_filename+" can't find.")

    if file_exist:
        source_input = file.read().split()
        source_to_int = list(map(int, source_input)) 
        file.close()

        seperate_list = Split_File(source_to_int, int(splitNum))

        sorted = queue.Queue()
        thread_list = []

        t1_start = perf_counter() # timer

        # bubble sort
        for i in range(int(splitNum)):
            thread = td.Thread(target=BubbleSort, args=(seperate_list[i], sorted))
            thread_list.append(thread)
    
        for t in thread_list:
            t.start()
    
        for t in thread_list: # waiting all threads finish
            t.join()
    
        merge_thread_list = []

        for i in range(int(splitNum)-1): # merge sort will do splitNum-1 times
            left = sorted.get()
            right = sorted.get()
            merge_thread_list.append(td.Thread(target=Merge, args=(left, right, sorted)))
            merge_thread_list[i].start()
            print("start thread", i, '\n\n') # for testing

        for i in range(int(splitNum)-1):       
            merge_thread_list[i].join()

        t1_stop = perf_counter() # timer
        cputime = t1_stop - t1_start
        print("CPU Time:", cputime)
        WriteFile(filename, "4", sorted.get(), cputime)    

# -----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    keep = True
    while keep:
        filename = input("請輸入檔案名稱(Input 0 exist):")
        if filename == "0":
            keep = False
        else:
            command = input("請輸入方法編號:(方法1, 方法2, 方法3, 方法4) ")
            if command == "1":
                Mission1(filename)
            elif command == "2":
                Mission2(filename)
            elif command == "3":
                Mission3(filename)
            elif command == "4":
                Mission4(filename)
            else:
                print("Sorry! No this option. ")
